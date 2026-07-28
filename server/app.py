from flask import request, jsonify, make_response
from datetime import datetime
from marshmallow import ValidationError

from config import create_app, db
from models import (
    Workout, Exercise, WorkoutExercise,
    workout_schema, workouts_schema,
    exercise_schema, exercises_schema,
    workout_exercise_schema
)

app = create_app()


@app.route('/workouts', methods=['GET', 'POST'])
def handle_workouts():
    if request.method == 'GET':
        workouts = Workout.query.all()
        return make_response(workouts_schema.dump(workouts), 200)

    elif request.method == 'POST':
        data = request.get_json() or {}
        try:
           
            if 'date' in data and isinstance(data['date'], str):
                data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()

            new_workout = workout_schema.load(data, session=db.session)
            db.session.add(new_workout)
            db.session.commit()
            return make_response(workout_schema.dump(new_workout), 201)

        except (ValidationError, ValueError) as err:
            db.session.rollback()
            errors = err.messages if isinstance(err, ValidationError) else str(err)
            return make_response(jsonify({"errors": errors}), 400)


@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def handle_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    if request.method == 'GET':
    
        return make_response(workout_schema.dump(workout), 200)

    elif request.method == 'DELETE':
       
        db.session.delete(workout)
        db.session.commit()
        return make_response(jsonify({"message": f"Workout {id} and associated exercise entries deleted successfully."}), 200)



@app.route('/exercises', methods=['GET', 'POST'])
def handle_exercises():
    if request.method == 'GET':
        exercises = Exercise.query.all()
        return make_response(exercises_schema.dump(exercises), 200)

    elif request.method == 'POST':
        data = request.get_json() or {}
        try:
            new_exercise = exercise_schema.load(data, session=db.session)
            db.session.add(new_exercise)
            db.session.commit()
            return make_response(exercise_schema.dump(new_exercise), 201)

        except (ValidationError, ValueError) as err:
            db.session.rollback()
            errors = err.messages if isinstance(err, ValidationError) else str(err)
            return make_response(jsonify({"errors": errors}), 400)


@app.route('/exercises/<int:id>', methods=['GET', 'DELETE'])
def handle_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    if request.method == 'GET':
        return make_response(exercise_schema.dump(exercise), 200)

    elif request.method == 'DELETE':
       
        db.session.delete(exercise)
        db.session.commit()
        return make_response(jsonify({"message": f"Exercise {id} and associated workout entries deleted successfully."}), 200)



@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return make_response(jsonify({"error": "Workout or Exercise not found"}), 404)

    data = request.get_json() or {}
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id

    try:
        new_entry = workout_exercise_schema.load(data, session=db.session)
        db.session.add(new_entry)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(new_entry), 201)

    except (ValidationError, ValueError) as err:
        db.session.rollback()
        errors = err.messages if isinstance(err, ValidationError) else str(err)
        return make_response(jsonify({"errors": errors}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)