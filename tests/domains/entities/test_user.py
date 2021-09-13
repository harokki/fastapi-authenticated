import pytest

from app.domains.entities.user import User
from app.domains.exceptions import ValidationError


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

    assert repr(user) == "User('john', 'john@example.com', 'ジョン', True)"


def test_get_hashed_password():
    hashed = User.get_hashed_password("plain")

    assert type(hashed) is str


def test_verify_password():
    hashed = User.get_hashed_password("plain")

    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password=hashed,
        created_by="john",
    )

    assert user.verify_password("plain") is True


@pytest.mark.parametrize(
    "username,message",
    [
        ("あいう", "only alphanumeric, underscore and hyphen is ok"),
        ("", "must be 1 or more and 32 or less"),
        ("t" * 33, "must be 1 or more and 32 or less"),
    ],
)
def test_validate_username(username, message):
    with pytest.raises(ValidationError) as ex_info:
        User(
            username=username,
            email="a@example.com",
            account_name="a",
            hashed_password="a",
            created_by="a",
        )

    assert ex_info.value.expression == username
    assert ex_info.value.code == "VALIDATION_ERROR"
    assert ex_info.value.message == message
