from datetime import timedelta

import pytest

from config import DEV_JWT_SECRET_KEY
from factory import create_app

PROD_ENV = {
    "SECRET_KEY": "real-secret",
    "JWT_SECRET_KEY": "real-jwt-secret-that-is-long-enough-123",
    "DOCTOR_INVITATION_CODE": "real-invite",
    "DATABASE_URL": "sqlite:///:memory:",
}


@pytest.fixture
def prod_env(monkeypatch):
    for key in ("RENDER", "FLASK_ENV", "APP_ENV"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("RENDER", "true")
    for key, value in PROD_ENV.items():
        monkeypatch.setenv(key, value)
    return monkeypatch


def test_defaults(app):
    assert app.config["CLINIC_TIMEZONE"] == "Asia/Kolkata"
    assert app.config["JWT_ACCESS_TOKEN_EXPIRES"] == timedelta(hours=8)


def test_invalid_timezone_fails_fast():
    with pytest.raises(RuntimeError, match="CLINIC_TIMEZONE"):
        create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                    "CLINIC_TIMEZONE": "Mars/Olympus"})


def test_production_with_all_secrets_starts(prod_env):
    assert create_app() is not None


@pytest.mark.parametrize("missing", list(PROD_ENV))
def test_production_missing_secret_fails(prod_env, missing):
    prod_env.delenv(missing)
    with pytest.raises(RuntimeError, match=missing):
        create_app()


def test_production_dev_default_secret_fails(prod_env):
    prod_env.setenv("JWT_SECRET_KEY", DEV_JWT_SECRET_KEY)
    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY is still the dev default"):
        create_app()


def test_flask_env_production_also_enforced(prod_env):
    prod_env.delenv("RENDER")
    prod_env.setenv("FLASK_ENV", "production")
    prod_env.delenv("SECRET_KEY")
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app()
