from fastapi.testclient import TestClient


def test_create_user_by_admin(
    client: TestClient, create_root_and_guest_user, admin_token_headers
):
    data = {
        "username": "anny",
        "email": "anny@example.com",
        "account_name": "アニー",
        "password": "plain",
    }

    r = client.post("/users", headers=admin_token_headers, json=data)

    json = r.json()
    assert r.status_code == 200
    assert json["username"] == data["username"]
    assert json["email"] == data["email"]
    assert json["account_name"] == data["account_name"]
    assert json["is_active"] is True
    assert json["created_at"]
    assert json["created_by"] == "john"
    assert json["updated_at"]
    assert json["updated_by"] == "john"


def test_create_exists_user_by_admin_return_422_error(
    client: TestClient, create_root_and_guest_user, admin_token_headers
):
    data = {
        "username": "john",
        "email": "john@example.com",
        "account_name": "ジョン",
        "password": "plain",
    }

    r = client.post("/users", headers=admin_token_headers, json=data)

    json = r.json()
    assert r.status_code == 422
    assert json["detail"] == "username or email already Exists"


def test_create_user_by_guest_returns_401_error(
    client: TestClient, create_root_and_guest_user, guest_token_headers
):
    data = {
        "username": "anny",
        "email": "anny@example.com",
        "account_name": "アニー",
        "password": "plain",
    }

    r = client.post("/users", headers=guest_token_headers, json=data)

    json = r.json()
    assert r.status_code == 401
    assert json["detail"] == "Not enough permissions"
