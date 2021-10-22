from fastapi.testclient import TestClient


def test_get_access_token_return_200(client: TestClient, create_root_and_guest_user):
    login_data = {"username": "john", "password": "plain"}

    r = client.post("/token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_with_fail_password_return_401(
    client: TestClient, create_root_and_guest_user
):
    login_data = {"username": "john", "password": "failpassword"}

    r = client.post("/token", data=login_data)
    tokens = r.json()
    assert r.status_code == 401
    assert "detail" in tokens
    assert tokens["detail"] == "Incorrect username or password"


def test_get_access_token_with_not_exist_username_return_401(
    client: TestClient, create_root_and_guest_user
):
    login_data = {"username": "not_exist", "password": "plain"}

    r = client.post("/token", data=login_data)
    tokens = r.json()
    assert r.status_code == 401
    assert "detail" in tokens
    assert tokens["detail"] == "Incorrect username or password"
