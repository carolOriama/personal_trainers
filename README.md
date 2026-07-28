# Workout Tracker API

A RESTful backend API for personal trainers to track workouts, exercises, and performance sets built with Flask, SQLAlchemy, and Marshmallow.

## Features
- Full CRUD support for Workouts and Exercises (excluding update per design spec).
- Many-to-many relationship mapping using `WorkoutExercises` as a join table.
- Multi-tier validations: Database Constraints, SQLAlchemy Model `@validates`, and Marshmallow Schemas.
- Cascading deletions for associated entries.

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pipenv install

2. **Activate Virtual Environment**
pipenv shell

3.**Initialize Database and Run Migrations**
cd server
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade head
cd ..