from app.domains.entities.user import User


def test_initialize_user():
    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="aaaaa",
        created_by="john",
    )

    assert user.username == "john"
    assert user.email == "john@example.com"
    assert user.account_name == "ジョン"
    assert user.hashed_password == "aaaaa"
    assert user.is_active is True
    assert user.created_by == "john"
    assert user.created_at
    assert user.updated_by == "john"
    assert user.updated_at
