# Workout Tracker API

A RESTful backend API for personal trainers to track workouts, exercises, and workout-specific exercise details. The application is built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow.

## Project Description

This API enables trainers to:
- Create, list, and delete workouts.
- Create, list, and delete reusable exercises.
- Attach exercises to workouts with reps, sets, and duration metadata.
- Validate request, model, and database-level integrity.

## Installation

1. Activate the project virtual environment.
2. Install the required packages:

```bash
./env/bin/python -m pip install Flask==2.2.2 Flask-Migrate==3.1.0 flask-sqlalchemy==3.0.3 Werkzeug==2.2.2 importlib-metadata==6.0.0 importlib-resources==5.10.0 ipdb==0.13.9 marshmallow==3.20.1 marshmallow-sqlalchemy==0.28.2
```

## Database Setup

From the `server/` directory:

```bash
export PYTHONPATH=.
../env/bin/python -m flask --app app db init
../env/bin/python -m flask --app app db migrate -m "initial workout tracker schema"
../env/bin/python -m flask --app app db upgrade head
```

## Seed the Database

```bash
cd server
export PYTHONPATH=.
../env/bin/python seed.py
```

## Run the API

```bash
cd server
export PYTHONPATH=.
../env/bin/python app.py
```

The app runs on `http://127.0.0.1:5555`.

## API Endpoints

- `GET /workouts` — list all workouts
- `GET /workouts/<id>` — fetch one workout and its attached exercise details
- `POST /workouts` — create a workout
- `DELETE /workouts/<id>` — delete a workout
- `GET /exercises` — list all exercises
- `GET /exercises/<id>` — fetch one exercise and its associated workouts
- `POST /exercises` — create an exercise
- `DELETE /exercises/<id>` — delete an exercise
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` — attach an exercise to a workout with reps, sets, and duration

## Validation Notes

The backend includes multiple validation layers:
- Database table constraints via `CheckConstraint` and `UniqueConstraint`
- SQLAlchemy model-level `@validates` checks
- Marshmallow request payload validation on POST routes