from app.domains.entities.user import User
from app.domains.repositories.user_repository import UserRepository


class UserApplicationService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def get_user(self, username: str) -> User:
        user = self._user_repository.find_by_username(username)
        return user
