from marshmallow import Schema, fields, validate, ValidationError, pre_load, post_load

from models import Exercise, Workout, WorkoutExercise


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1))
    category = fields.String(required=True, validate=validate.Length(min=1))
    equipment_needed = fields.Boolean(required=True)

    @pre_load
    def normalize_payload(self, data, **kwargs):
        if not isinstance(data, dict):
            raise ValidationError("JSON object required")
        if "name" in data and isinstance(data["name"], str):
            data["name"] = data["name"].strip()
        if "category" in data and isinstance(data["category"], str):
            data["category"] = data["category"].strip()
        if not data.get("name") or not str(data["name"]).strip():
            raise ValidationError({"name": ["Exercise name must not be empty"]})
        if not data.get("category") or not str(data["category"]).strip():
            raise ValidationError({"category": ["Exercise category must not be empty"]})
        if "equipment_needed" not in data or not isinstance(data.get("equipment_needed"), bool):
            raise ValidationError({"equipment_needed": ["equipment_needed must be a boolean"]})
        return data

    @post_load
    def build_exercise(self, data, **kwargs):
        return Exercise(**data)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1))
    notes = fields.String(allow_none=True)

    @pre_load
    def normalize_payload(self, data, **kwargs):
        if not isinstance(data, dict):
            raise ValidationError("JSON object required")
        if data.get("duration_minutes") is None:
            raise ValidationError({"duration_minutes": ["duration_minutes is required"]})
        if int(data["duration_minutes"]) < 1:
            raise ValidationError({"duration_minutes": ["duration_minutes must be at least 1"]})
        if data.get("date") is None:
            raise ValidationError({"date": ["date is required"]})
        return data

    @post_load
    def build_workout(self, data, **kwargs):
        return Workout(**data)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Integer(required=True, validate=validate.Range(min=1))
    sets = fields.Integer(required=True, validate=validate.Range(min=1))
    duration_seconds = fields.Integer(required=True, validate=validate.Range(min=0))

    @pre_load
    def normalize_payload(self, data, **kwargs):
        if not isinstance(data, dict):
            raise ValidationError("JSON object required")
        if data.get("reps") is None or int(data["reps"]) < 1:
            raise ValidationError({"reps": ["reps must be at least 1"]})
        if data.get("sets") is None or int(data["sets"]) < 1:
            raise ValidationError({"sets": ["sets must be at least 1"]})
        if data.get("duration_seconds") is None or int(data["duration_seconds"]) < 0:
            raise ValidationError({"duration_seconds": ["duration_seconds must be 0 or greater"]})
        return data

    @post_load
    def build_workout_exercise(self, data, **kwargs):
        return WorkoutExercise(**data)


exercise_schema = ExerciseSchema()
exercise_list_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workout_list_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercise_list_schema = WorkoutExerciseSchema(many=True)
