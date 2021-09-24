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


def test_get_role_names():
    hashed = User.get_hashed_password("plain")

    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password=hashed,
        created_by="john",
    )

    assert user.get_role_names() == []


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


@pytest.mark.parametrize(
    "email,message",
    [
        ("john'semail", "illegal email format"),
        ("", "illegal email format"),
        ("t" * 245 + "@example.com", "must be 1 or more and 256 or less"),
    ],
)
def test_validate_email(email, message):
    with pytest.raises(ValidationError) as ex_info:
        User(
            username="john",
            email=email,
            account_name="a",
            hashed_password="a",
            created_by="a",
        )

    assert ex_info.value.expression == email
    assert ex_info.value.code == "VALIDATION_ERROR"
    assert ex_info.value.message == message


@pytest.mark.parametrize(
    "account_name,message",
    [
        ("", "must be 1 or more and 32 or less"),
        ("t" * 33, "must be 1 or more and 32 or less"),
    ],
)
def test_validate_account_name(account_name, message):
    with pytest.raises(ValidationError) as ex_info:
        User(
            username="john",
            email="john@example.com",
            account_name=account_name,
            hashed_password="a",
            created_by="a",
        )

    assert ex_info.value.expression == account_name
    assert ex_info.value.code == "VALIDATION_ERROR"
    assert ex_info.value.message == message


@pytest.mark.parametrize(
    "hashed_password,message",
    [
        ("", "must be 1 or more and 64 or less"),
        ("t" * 65, "must be 1 or more and 64 or less"),
    ],
)
def test_validate_hashed_password(hashed_password, message):
    with pytest.raises(ValidationError) as ex_info:
        User(
            username="john",
            email="john@example.com",
            account_name="ジョン",
            hashed_password=hashed_password,
            created_by="a",
        )

    assert ex_info.value.expression == hashed_password
    assert ex_info.value.code == "VALIDATION_ERROR"
    assert ex_info.value.message == message


@pytest.mark.parametrize(
    "created_by,message",
    [
        ("", "must be 1 or more and 32 or less"),
        ("t" * 33, "must be 1 or more and 32 or less"),
    ],
)
def test_validate_created_by(created_by, message):
    with pytest.raises(ValidationError) as ex_info:
        User(
            username="john",
            email="john@example.com",
            account_name="ジョン",
            hashed_password="a",
            created_by=created_by,
        )

    assert ex_info.value.expression == created_by
    assert ex_info.value.code == "VALIDATION_ERROR"
    assert ex_info.value.message == message


def test_get_user_with_roles():
    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="aaaaa",
        created_by="john",
    )

    user_with_roles = user.get_user_with_roles()

    assert user_with_roles.username == "john"
    assert user_with_roles.email == "john@example.com"
    assert user_with_roles.account_name == "ジョン"
    assert user_with_roles.is_active is True
    assert user_with_roles.roles == []
    assert user_with_roles.created_by == "john"
    assert user_with_roles.created_at
    assert user_with_roles.updated_by == "john"
    assert user_with_roles.updated_at
