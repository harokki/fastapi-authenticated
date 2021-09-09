from app.domains.entities.user import User


def test_initialize_user():
    user = User(
        username="john",
        email="john@example.com",
        hashed_password="aaaaa",
        is_active=True,
    )

    assert user.username == "john"
    assert user.email == "john@example.com"
    assert user.hashed_password == "aaaaa"
    assert user.is_active is True
