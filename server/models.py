from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates


db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"
    __table_args__ = (
        db.CheckConstraint("length(name) >= 1", name="exercise_name_not_empty"),
        db.CheckConstraint("length(category) >= 1", name="exercise_category_not_empty"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    category = db.Column(db.String(80), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
        overlaps="workouts",
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        overlaps="workout_exercises",
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not str(value).strip():
            raise ValueError("Exercise name must not be empty")
        return str(value).strip()

    @validates("category")
    def validate_category(self, key, value):
        if not value or not str(value).strip():
            raise ValueError("Exercise category must not be empty")
        return str(value).strip()


class Workout(db.Model):
    __tablename__ = "workouts"
    __table_args__ = (
        db.CheckConstraint("duration_minutes >= 1", name="workout_duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
        overlaps="exercises",
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        overlaps="workout_exercises",
    )

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        if value is None or value < 1:
            raise ValueError("Workout duration_minutes must be at least 1")
        return value

    @validates("notes")
    def validate_notes(self, key, value):
        if value is not None and not str(value).strip():
            return None
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    __table_args__ = (
        db.CheckConstraint("reps >= 1", name="workout_exercise_reps_positive"),
        db.CheckConstraint("sets >= 1", name="workout_exercise_sets_positive"),
        db.CheckConstraint("duration_seconds >= 0", name="workout_exercise_duration_non_negative"),
        db.UniqueConstraint("workout_id", "exercise_id", name="unique_workout_exercise_pair"),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False, default=0)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps")
    def validate_reps(self, key, value):
        if value is None or value < 1:
            raise ValueError("reps must be at least 1")
        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if value is None or value < 1:
            raise ValueError("sets must be at least 1")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is None or value < 0:
            raise ValueError("duration_seconds must be 0 or greater")
        return value
