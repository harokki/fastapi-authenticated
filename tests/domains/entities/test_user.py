from app.domains.entities.user import User


def test_initialize_user():
    user = User(
        id=123, email="1234@example.com", hashed_password="aaaaa", is_active=True
    )

    assert user.id == 123
    assert user.email == "1234@example.com"
    assert user.hashed_password == "aaaaa"
    assert user.is_active is True
    assert user.items == []
