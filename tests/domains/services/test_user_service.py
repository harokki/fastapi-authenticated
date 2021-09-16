from unittest.mock import MagicMock

from app.domains.entities.user import User
from app.domains.services.user_service import UserService
from app.infrastructures.repositories.user_repository import SAUserRepository


def test_exists_is_true_if_username_is_exist():
    user = User("john", "john@example.com", "ジョン", "aaaa", "john")
    user_repository = SAUserRepository(MagicMock())
    user_repository.find_by_username = MagicMock(return_value=user)
    user_repository.find_by_email = MagicMock(return_value=None)

    user_service = UserService(user_repository)

    is_exist = user_service.exists("john", "john@example.com")

    assert is_exist is True


def test_exists_is_true_if_email_is_exist():
    user = User("john", "john@example.com", "ジョン", "aaaa", "john")
    user_repository = SAUserRepository(MagicMock())
    user_repository.find_by_username = MagicMock(return_value=None)
    user_repository.find_by_email = MagicMock(return_value=user)

    user_service = UserService(user_repository)

    is_exist = user_service.exists("john", "john@example.com")

    assert is_exist is True


def test_exists_is_false_if_user_is_not_exist():
    user_repository = SAUserRepository(MagicMock())
    user_repository.find_by_username = MagicMock(return_value=None)
    user_repository.find_by_email = MagicMock(return_value=None)

    user_service = UserService(user_repository)

    is_exist = user_service.exists("john", "john@example.com")

    assert is_exist is False
