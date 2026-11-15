"""Request validation helpers.

Raise ValidationError from controllers/routes; the registered handler turns it into
400 {"error": "...", "fields": {field: message}}.
"""
from datetime import date, datetime, time

from flask import jsonify, request


class ValidationError(Exception):
    def __init__(self, message: str = "Invalid request", fields: dict | None = None, status: int = 400):
        super().__init__(message)
        self.message = message
        self.fields = fields or {}
        self.status = status

    def to_response(self):
        body = {"error": self.message}
        if self.fields:
            body["fields"] = self.fields
        return jsonify(body), self.status


def register_validation_handler(app) -> None:
    @app.errorhandler(ValidationError)
    def _handle_validation_error(err: ValidationError):
        return err.to_response()


def get_json_body() -> dict:
    """Return the JSON object body, or raise if missing / not an object."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")
    return data


def _is_blank(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def require(data: dict, *fields: str) -> None:
    missing = {f: "This field is required" for f in fields if _is_blank(data.get(f))}
    if missing:
        raise ValidationError("Missing required fields", missing)


def parse_date(value, field: str = "date") -> date:
    """Strict YYYY-MM-DD."""
    if not isinstance(value, str):
        raise ValidationError("Invalid date", {field: "Use format YYYY-MM-DD"})
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("Invalid date", {field: "Use format YYYY-MM-DD"})


def parse_time(value, field: str = "time") -> time:
    """Strict 24h HH:MM."""
    if not isinstance(value, str):
        raise ValidationError("Invalid time", {field: "Use 24h format HH:MM"})
    try:
        return datetime.strptime(value.strip(), "%H:%M").time()
    except ValueError:
        raise ValidationError("Invalid time", {field: "Use 24h format HH:MM"})


def parse_int(value, field: str, min_value: int | None = None, max_value: int | None = None) -> int:
    """Accepts ints or digit strings; rejects bools/floats."""
    if isinstance(value, bool):
        raise ValidationError("Invalid number", {field: "Must be a whole number"})
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        value = int(value.strip())
    if not isinstance(value, int):
        raise ValidationError("Invalid number", {field: "Must be a whole number"})
    if min_value is not None and value < min_value:
        raise ValidationError("Invalid number", {field: f"Must be at least {min_value}"})
    if max_value is not None and value > max_value:
        raise ValidationError("Invalid number", {field: f"Must be at most {max_value}"})
    return value
