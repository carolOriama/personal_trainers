from config import db, ma
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from marshmallow import fields, validate, ValidationError



class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)


    workout_exercises = db.relationship(
        'WorkoutExercise', 
        back_populates='exercise', 
        cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout', 
        secondary='workout_exercises', 
        back_populates='exercises'
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Cardio', 'Strength', 'Flexibility', 'Balance', 'Calisthenics']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

  
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )


    workout_exercises = db.relationship(
        'WorkoutExercise', 
        back_populates='workout', 
        cascade='all, delete-orphan'
    )
    exercises = db.relationship(
        'Exercise', 
        secondary='workout_exercises', 
        back_populates='workouts'
    )

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration <= 0:
            raise ValueError("Workout duration must be a positive integer.")
        return duration


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)


    __table_args__ = (
        CheckConstraint('reps >= 0', name='check_reps_non_negative'),
        CheckConstraint('sets >= 0', name='check_sets_non_negative'),
    )

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')


    @validates('reps', 'sets', 'duration_seconds')
    def validate_metrics(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key.capitalize()} cannot be negative.")
        return value




class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True

  
    reps = fields.Int(validate=validate.Range(min=0, error="Reps must be 0 or greater."))
    sets = fields.Int(validate=validate.Range(min=0, error="Sets must be 0 or greater."))
    duration_seconds = fields.Int(validate=validate.Range(min=0, error="Duration seconds must be 0 or greater."))

    exercise = fields.Nested('ExerciseSchema', only=('id', 'name', 'category', 'equipment_needed'))


class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True


    name = fields.Str(
        required=True, 
        validate=validate.Length(min=2, error="Name must be at least 2 characters long.")
    )
    category = fields.Str(
        required=True, 
        validate=validate.OneOf(
            ['Cardio', 'Strength', 'Flexibility', 'Balance', 'Calisthenics'],
            error="Invalid category."
        )
    )
    equipment_needed = fields.Bool(required=True)

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, exclude=('exercise',))


class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True


    duration_minutes = fields.Int(
        required=True, 
        validate=validate.Range(min=1, error="Duration must be at least 1 minute.")
    )
    date = fields.Date(required=True)

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, exclude=('workout',))



exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()