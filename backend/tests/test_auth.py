from fastapi.testclient import TestClient


def test_register_and_me(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register",
        json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "analytic123"},
    )
    assert response.status_code == 201
    token = response.json()["access_token"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    body = me.json()
    assert body["email"] == "ada@example.com"
    assert body["name"] == "Ada Lovelace"
    assert "password" not in body


def test_login_and_duplicate_register(client: TestClient) -> None:
    payload = {"name": "Grace Hopper", "email": "grace@example.com", "password": "compiler1"}
    assert client.post("/api/auth/register", json=payload).status_code == 201
    duplicate = client.post("/api/auth/register", json=payload)
    assert duplicate.status_code == 409
    login = client.post("/api/auth/login", json={"email": "grace@example.com", "password": "compiler1"})
    assert login.status_code == 200
    bad = client.post("/api/auth/login", json={"email": "grace@example.com", "password": "wrongpass"})
    assert bad.status_code == 401


def test_protected_route_requires_token(client: TestClient) -> None:
    response = client.get("/api/resumes")
    assert response.status_code == 401
