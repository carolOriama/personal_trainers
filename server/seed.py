#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():
    db.drop_all()
    db.create_all()

    squat = Exercise(name="Squat", category="Legs", equipment_needed=False)
    press = Exercise(name="Push Up", category="Upper Body", equipment_needed=False)
    row = Exercise(name="Bent-Over Row", category="Back", equipment_needed=True)
    db.session.add_all([squat, press, row])
    db.session.commit()

    workout_1 = Workout(date=date(2026, 7, 28), duration_minutes=40, notes="Morning strength session")
    workout_2 = Workout(date=date(2026, 7, 29), duration_minutes=30, notes="Cardio + mobility")
    db.session.add_all([workout_1, workout_2])
    db.session.commit()

    link_1 = WorkoutExercise(workout_id=workout_1.id, exercise_id=squat.id, reps=5, sets=4, duration_seconds=0)
    link_2 = WorkoutExercise(workout_id=workout_1.id, exercise_id=press.id, reps=8, sets=3, duration_seconds=0)
    link_3 = WorkoutExercise(workout_id=workout_2.id, exercise_id=row.id, reps=10, sets=3, duration_seconds=45)
    db.session.add_all([link_1, link_2, link_3])
    db.session.commit()

    print("Seed data loaded.")
