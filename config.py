
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-dev-secret")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///local.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Resend
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")

    # Doctor Registration
    DOCTOR_INVITATION_CODE = os.getenv("DOCTOR_INVITATION_CODE", "DOC2024SECRET")