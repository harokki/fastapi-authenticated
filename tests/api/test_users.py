from fastapi.testclient import TestClient


def test_create_user(
    client: TestClient, create_root_and_guest_user, admin_token_headers
):
    data = {
        "username": "anny",
        "email": "anny@example.com",
        "account_name": "アニー",
        "is_active": True,
        "password": "plain",
    }

    r = client.post("/users", headers=admin_token_headers, json=data)

    json = r.json()
    assert r.status_code == 200
    assert json["username"] == data["username"]
    assert json["email"] == data["email"]
    assert json["account_name"] == data["account_name"]
    assert json["is_active"] == data["is_active"]
    assert json["created_at"]
    assert json["created_by"] == "john"
    assert json["updated_at"]
    assert json["updated_by"] == "john"
