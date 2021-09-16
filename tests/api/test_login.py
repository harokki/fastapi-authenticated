from fastapi.testclient import TestClient


def test_get_access_token(client: TestClient, create_root_user):
    login_data = {"username": "john", "password": "plain"}

    r = client.post("/token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
