from fastapi.testclient import TestClient


def test_create_user_by_admin(
    client: TestClient, admin_token_headers, delete_other_than_default_user
):
    data = {
        "username": "anny",
        "email": "anny@example.com",
        "account_name": "アニー",
        "password": "plainpassword",
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


def test_creat_user_by_admin_check_required_field(
    client: TestClient, admin_token_headers
):
    data = {"dummy": "dummy"}

    r = client.post("/users", headers=admin_token_headers, json=data)

    json = r.json()
    expected = {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "email"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "account_name"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "password"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }

    assert r.status_code == 422
    assert json == expected


def test_creat_user_by_admin_check_min_length(client: TestClient, admin_token_headers):
    data = {
        "username": "",
        "email": "",
        "account_name": "",
        "password": "",
    }

    r = client.post("/users", headers=admin_token_headers, json=data)

    json = r.json()
    expected = {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "ensure this value has at least 1 characters",
                "type": "value_error.any_str.min_length",
                "ctx": {"limit_value": 1},
            },
            {
                "loc": ["body", "email"],
                "msg": "ensure this value has at least 1 characters",
                "type": "value_error.any_str.min_length",
                "ctx": {"limit_value": 1},
            },
            {
                "loc": ["body", "account_name"],
                "msg": "ensure this value has at least 1 characters",
                "type": "value_error.any_str.min_length",
                "ctx": {"limit_value": 1},
            },
            {
                "loc": ["body", "password"],
                "msg": "ensure this value has at least 8 characters",
                "type": "value_error.any_str.min_length",
                "ctx": {"limit_value": 8},
            },
        ]
    }

    assert r.status_code == 422
    assert json == expected


def test_creat_user_by_admin_check_max_length(client: TestClient, admin_token_headers):
    data = {
        "username": "a" * 33,
        "email": "a" * 257,
        "account_name": "a" * 33,
        "password": "a" * 65,
    }

    r = client.post("/users", headers=admin_token_headers, json=data)

    json = r.json()
    expected = {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "ensure this value has at most 32 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {"limit_value": 32},
            },
            {
                "loc": ["body", "email"],
                "msg": "ensure this value has at most 256 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {"limit_value": 256},
            },
            {
                "loc": ["body", "account_name"],
                "msg": "ensure this value has at most 32 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {"limit_value": 32},
            },
            {
                "loc": ["body", "password"],
                "msg": "ensure this value has at most 64 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {"limit_value": 64},
            },
        ]
    }

    assert r.status_code == 422
    assert json == expected


def test_creat_user_by_admin_check_invalid_username_email(
    client: TestClient, admin_token_headers
):
    data = {
        "username": "john$",
        "email": "johnemail",
        "account_name": "ジョン",
        "password": "plainplain",
    }

    r = client.post("/users", headers=admin_token_headers, json=data)

    json = r.json()
    expected = {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "only alphanumeric, underscore and hyphen is ok",
                "type": "value_error",
            },
            {
                "loc": ["body", "email"],
                "msg": "illegal email format",
                "type": "value_error",
            },
        ]
    }

    assert r.status_code == 422
    assert json == expected


def test_create_user_by_admin_check_request_body_type(
    client: TestClient, admin_token_headers
):
    data = {
        "username": 1,
        "email": 1,
        "account_name": 1,
        "password": 1,
    }

    r = client.post("/users", headers=admin_token_headers, json=data)

    json = r.json()
    expected = {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "str type expected",
                "type": "type_error.str",
            },
            {
                "loc": ["body", "email"],
                "msg": "str type expected",
                "type": "type_error.str",
            },
            {
                "loc": ["body", "account_name"],
                "msg": "str type expected",
                "type": "type_error.str",
            },
            {
                "loc": ["body", "password"],
                "msg": "str type expected",
                "type": "type_error.str",
            },
        ]
    }
    assert r.status_code == 422
    assert json == expected


def test_create_exists_user_by_admin_return_422_error(
    client: TestClient, admin_token_headers
):
    data = {
        "username": "john",
        "email": "john@example.com",
        "account_name": "ジョン",
        "password": "plainpassword",
    }

    r = client.post("/users", headers=admin_token_headers, json=data)

    json = r.json()
    assert r.status_code == 422
    assert json["detail"] == "username or email already Exists"


def test_create_user_by_guest_returns_401_error(
    client: TestClient, guest_token_headers
):
    data = {
        "username": "anny",
        "email": "anny@example.com",
        "account_name": "アニー",
        "password": "plainpassword",
    }

    r = client.post("/users", headers=guest_token_headers, json=data)

    json = r.json()
    assert r.status_code == 401
    assert json["detail"] == "Not enough permissions"


def test_get_users(client: TestClient, admin_token_headers):
    r = client.get("/users", headers=admin_token_headers)

    json = r.json()
    user1 = json[0]
    user2 = json[1]

    assert r.status_code == 200
    assert len(json) == 2

    assert user1["username"] == "john"
    assert user1["email"] == "john@example.com"
    assert user1["account_name"] == "ジョン"
    assert user1["is_active"] is True
    assert user1["created_at"]
    assert user1["created_by"] == "default"
    assert user1["updated_at"]
    assert user1["updated_by"] == "default"

    assert user2["username"] == "emma"
    assert user2["email"] == "emma@example.com"
    assert user2["account_name"] == "エマ"
    assert user2["is_active"] is True
    assert user2["created_at"]
    assert user2["created_by"] == "default"
    assert user2["updated_at"]
    assert user2["updated_by"] == "default"
