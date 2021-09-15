import pytest

from app.domains.entities.role import Role
from app.domains.entities.user import User
from app.domains.entities.user_role import UserRole
from app.domains.exceptions import ValidationError


def test_initialize_user_role():
    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="aaaaa",
        created_by="john",
    )
    role = Role("Admin", "")
    user_role = UserRole(username=user.username, role_id=role.id)

    assert user_role.username == user.username
    assert user_role.role_id == role.id


@pytest.mark.parametrize(
    "username,message",
    [
        ("", "must be 1 or more and 32 or less"),
        ("t" * 33, "must be 1 or more and 32 or less"),
    ],
)
def test_validate_username(username, message):
    with pytest.raises(ValidationError) as ex_info:
        UserRole(username, "aaaaaa")

    assert ex_info.value.expression == username
    assert ex_info.value.code == "VALIDATION_ERROR"
    assert ex_info.value.message == message


@pytest.mark.parametrize(
    "role_id,message",
    [
        ("", "must be 1 or more and 36 or less"),
        ("t" * 37, "must be 1 or more and 36 or less"),
    ],
)
def test_validate_role_id(role_id, message):
    with pytest.raises(ValidationError) as ex_info:
        UserRole("john", role_id)

    assert ex_info.value.expression == role_id
    assert ex_info.value.code == "VALIDATION_ERROR"
    assert ex_info.value.message == message
