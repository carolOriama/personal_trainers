from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema,
    exercise_list_schema,
    workout_schema,
    workout_list_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/workouts", methods=["GET", "POST"])
def workouts():
    if request.method == "GET":
        workouts = Workout.query.order_by(Workout.id).all()
        result = workout_list_schema.dump(workouts)
        return jsonify(result)

    payload = request.get_json(force=True)
    try:
        workout = workout_schema.load(payload)
        db.session.add(workout)
        db.session.commit()
    except ValidationError as exc:
        return make_response(jsonify({"error": exc.messages}), 400)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"error": "Workout could not be created"}), 400)
    return make_response(jsonify(workout_schema.dump(workout)), 201)


@app.route("/workouts/<int:workout_id>", methods=["GET", "DELETE"])
def workout_by_id(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    if request.method == "GET":
        payload = workout_schema.dump(workout)
        payload["workout_exercises"] = [
            {
                "exercise_id": we.exercise_id,
                "exercise_name": we.exercise.name,
                "reps": we.reps,
                "sets": we.sets,
                "duration_seconds": we.duration_seconds,
            }
            for we in workout.workout_exercises
        ]
        return jsonify(payload)

    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout deleted"}), 200)


@app.route("/exercises", methods=["GET", "POST"])
def exercises():
    if request.method == "GET":
        exercises = Exercise.query.order_by(Exercise.id).all()
        result = exercise_list_schema.dump(exercises)
        return jsonify(result)

    payload = request.get_json(force=True)
    try:
        exercise = exercise_schema.load(payload)
        db.session.add(exercise)
        db.session.commit()
    except ValidationError as exc:
        return make_response(jsonify({"error": exc.messages}), 400)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"error": "Exercise could not be created"}), 400)
    return make_response(jsonify(exercise_schema.dump(exercise)), 201)


@app.route("/exercises/<int:exercise_id>", methods=["GET", "DELETE"])
def exercise_by_id(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)

    if request.method == "GET":
        payload = exercise_schema.dump(exercise)
        payload["associated_workouts"] = [
            {
                "workout_id": we.workout_id,
                "date": we.workout.date.isoformat(),
                "reps": we.reps,
                "sets": we.sets,
                "duration_seconds": we.duration_seconds,
            }
            for we in exercise.workout_exercises
        ]
        return jsonify(payload)

    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise deleted"}), 200)


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)

    payload = request.get_json(force=True)
    payload["workout_id"] = workout_id
    payload["exercise_id"] = exercise_id

    try:
        workout_exercise = workout_exercise_schema.load(payload)
        db.session.add(workout_exercise)
        db.session.commit()
    except ValidationError as exc:
        return make_response(jsonify({"error": exc.messages}), 400)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"error": "That exercise is already attached to this workout"}), 409)
    return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": str(error)}), 400)


@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({"error": "Internal server error"}), 500)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
