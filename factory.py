from flask import Flask
from flask_cors import CORS

from config import validate_config
from extensions import init_extensions
from routes import register_routes
from utils.validation import register_validation_handler


CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://docappointments.in",
    "https://www.docappointments.in",
]


def create_app(config_overrides: dict | None = None) -> Flask:
    """Build the Flask app. Env loading (.env) is the caller's job, so tests stay isolated."""
    app = Flask(__name__)
    app.config.from_object("config.Config")
    if config_overrides:
        app.config.update(config_overrides)
    validate_config(app)

    CORS(app, origins=CORS_ORIGINS, supports_credentials=True)

    init_extensions(app)
    register_routes(app)
    register_validation_handler(app)
    return app
