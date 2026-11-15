from tests.conftest import TEST_INVITE_CODE, TEST_PASSWORD


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_register_patient(client):
    res = client.post("/auth/register", json={
        "name": "Alice", "email": "alice@example.com",
        "password": TEST_PASSWORD, "role": "patient",
    })
    assert res.status_code == 201


def test_register_duplicate_email_conflicts(client, make_patient):
    make_patient(email="dup@example.com")
    res = client.post("/auth/register", json={
        "name": "Dup", "email": "dup@example.com",
        "password": TEST_PASSWORD, "role": "patient",
    })
    assert res.status_code == 409


def test_register_doctor_requires_valid_invite(client):
    base = {"name": "Dr Bob", "email": "bob@example.com", "password": TEST_PASSWORD, "role": "doctor"}
    assert client.post("/auth/register", json={**base, "invitation_code": "wrong"}).status_code == 403
    assert client.post("/auth/register", json={**base, "invitation_code": TEST_INVITE_CODE}).status_code == 201


def test_login_returns_token_with_role(client, make_patient):
    user = make_patient(email="login@example.com")
    res = client.post("/auth/login", json={"email": "login@example.com", "password": TEST_PASSWORD})
    assert res.status_code == 200
    token = res.get_json()["access_token"]

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.get_json()["id"] == user.id
    assert me.get_json()["role"] == "patient"


def test_login_wrong_password_rejected(client, make_patient):
    make_patient(email="wrongpw@example.com")
    res = client.post("/auth/login", json={"email": "wrongpw@example.com", "password": "nope"})
    assert res.status_code == 401


def test_fixtures_auth_header(client, make_doctor, auth_header):
    user, _ = make_doctor()
    res = client.get("/doctor/profile", headers=auth_header(user))
    assert res.status_code == 200
    assert res.get_json()["specialization"] == "General Practitioner"
