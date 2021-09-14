import pytest

from app.domains.entities.role import Role
from app.domains.exceptions import ValidationError


def test_initialize_role():
    role = Role("Admin", "admin user")

    assert role.name == "Admin"
    assert role.description == "admin user"


@pytest.mark.parametrize(
    "name,message",
    [
        ("", "must be 1 or more and 100 or less"),
        ("t" * 101, "must be 1 or more and 100 or less"),
    ],
)
def test_validate_name(name, message):
    with pytest.raises(ValidationError) as ex_info:
        Role(name, "user")

    assert ex_info.value.expression == name
    assert ex_info.value.code == "VALIDATION_ERROR"
    assert ex_info.value.message == message


@pytest.mark.parametrize(
    "description,message",
    [
        ("t" * 257, "must be 0 or more and 256 or less"),
    ],
)
def test_validate_description(description, message):
    with pytest.raises(ValidationError) as ex_info:
        Role("Admin", description)

    assert ex_info.value.expression == description
    assert ex_info.value.code == "VALIDATION_ERROR"
    assert ex_info.value.message == message
