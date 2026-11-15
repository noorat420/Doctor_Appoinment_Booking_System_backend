import os
from datetime import timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Dev-only fallbacks. In production these must be overridden by real env vars.
DEV_SECRET_KEY = "dev-secret"
DEV_JWT_SECRET_KEY = "jwt-dev-secret"
DEV_DOCTOR_INVITATION_CODE = "DOC2024SECRET"

REQUIRED_IN_PRODUCTION = {
    "SECRET_KEY": DEV_SECRET_KEY,
    "JWT_SECRET_KEY": DEV_JWT_SECRET_KEY,
    "DOCTOR_INVITATION_CODE": DEV_DOCTOR_INVITATION_CODE,
    "DATABASE_URL": None,
}


def is_production() -> bool:
    """Render sets RENDER=true automatically; FLASK_ENV/APP_ENV allow explicit opt-in."""
    return (
        os.getenv("RENDER", "").lower() == "true"
        or os.getenv("FLASK_ENV", "").lower() == "production"
        or os.getenv("APP_ENV", "").lower() == "production"
    )


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", DEV_SECRET_KEY)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", DEV_JWT_SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_HOURS", "8")))

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Neon closes idle connections; check before use and recycle periodically.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 300}

    # Resend
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")

    # Doctor registration
    DOCTOR_INVITATION_CODE = os.getenv("DOCTOR_INVITATION_CODE", DEV_DOCTOR_INVITATION_CODE)

    # Slot dates/times are clinic-local wall time in this zone.
    CLINIC_TIMEZONE = os.getenv("CLINIC_TIMEZONE", "Asia/Kolkata")


def validate_config(app) -> None:
    """Fail fast on startup instead of running with unsafe or broken settings."""
    tz_name = app.config.get("CLINIC_TIMEZONE")
    try:
        ZoneInfo(tz_name)
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        raise RuntimeError(f"CLINIC_TIMEZONE '{tz_name}' is not a valid IANA timezone")

    if app.config.get("TESTING") or not is_production():
        return

    problems = []
    for key, dev_default in REQUIRED_IN_PRODUCTION.items():
        if not os.getenv(key):
            problems.append(f"{key} is not set")
        elif dev_default is not None and os.getenv(key) == dev_default:
            problems.append(f"{key} is still the dev default")
    if problems:
        raise RuntimeError("Unsafe production config: " + "; ".join(problems))
