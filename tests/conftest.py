import itertools

import pytest
import resend
from flask_jwt_extended import create_access_token

from extensions import db
from factory import create_app
from repositories.doctor_repository import DoctorRepository
from repositories.user_repository import UserRepository
from utils.security import hash_password

TEST_PASSWORD = "Password123!"
TEST_INVITE_CODE = "TEST-INVITE"

_counter = itertools.count(1)


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-jwt-secret-key-that-is-at-least-32-bytes",
        "SECRET_KEY": "test-secret",
        "DOCTOR_INVITATION_CODE": TEST_INVITE_CODE,
        "RESEND_API_KEY": "test",
        "FROM_EMAIL": "test@example.com",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def sent_emails(monkeypatch):
    """Never hit Resend in tests; record outgoing emails instead."""
    outbox = []
    monkeypatch.setattr(resend.Emails, "send", lambda params: outbox.append(params) or {"id": "test"})
    return outbox


@pytest.fixture
def make_patient(app):
    def _make(name="Test Patient", email=None, password=TEST_PASSWORD):
        email = email or f"patient{next(_counter)}@example.com"
        return UserRepository.create(name=name, email=email,
                                     password_hash=hash_password(password), role="patient")
    return _make


@pytest.fixture
def make_doctor(app):
    """Returns (user, doctor)."""
    def _make(name="Test Doctor", email=None, password=TEST_PASSWORD,
              specialization="General Practitioner"):
        email = email or f"doctor{next(_counter)}@example.com"
        user = UserRepository.create(name=name, email=email,
                                     password_hash=hash_password(password), role="doctor")
        doctor = DoctorRepository.create(user_id=user.id, designation="Dr.",
                                         specialization=specialization)
        return user, doctor
    return _make


@pytest.fixture
def auth_header(app):
    def _header(user):
        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return {"Authorization": f"Bearer {token}"}
    return _header
