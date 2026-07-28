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

    # Relationships
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