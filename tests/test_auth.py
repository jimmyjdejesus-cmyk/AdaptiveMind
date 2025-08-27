from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def get_token(username: str, password: str) -> str:
    response = client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_workflow_requires_auth():
    response = client.get("/api/workflow/test")
    assert response.status_code == 401


def test_admin_access_logs():
    token = get_token("admin", "adminpass")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/logs", headers=headers)
    assert response.status_code == 200


def test_user_forbidden_logs():
    token = get_token("user", "userpass")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/logs", headers=headers)
    assert response.status_code == 403
