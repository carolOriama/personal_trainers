
from datetime import date
from sys import path
import os


path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))

from config import create_app, db
from models import Workout, Exercise, WorkoutExercise

app = create_app()

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding Exercises...")
    e1 = Exercise(name="Push Up", category="Calisthenics", equipment_needed=False)
    e2 = Exercise(name="Bench Press", category="Strength", equipment_needed=True)
    e3 = Exercise(name="Treadmill Run", category="Cardio", equipment_needed=True)
    e4 = Exercise(name="Plank", category="Calisthenics", equipment_needed=False)

    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    print("Seeding Workouts...")
    w1 = Workout(date=date(2026, 7, 20), duration_minutes=45, notes="Upper body hyper-focus.")
    w2 = Workout(date=date(2026, 7, 22), duration_minutes=30, notes="Morning cardio session.")

    db.session.add_all([w1, w2])
    db.session.commit()

    print("Seeding WorkoutExercises (Join Table)...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, reps=15, sets=3, duration_seconds=0)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e2.id, reps=10, sets=4, duration_seconds=0)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e3.id, reps=0, sets=1, duration_seconds=1800)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database successfully seeded!")