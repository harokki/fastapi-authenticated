from typing import List

from app.domains.entities.user import User
from app.domains.exceptions import DuplicationError
from app.domains.repositories.user_repository import UserRepository
from app.domains.services.user_service import UserService
from app.schemas.user import UserCreateSchema, UserWithRoleSchema


class UserApplicationService:
    def __init__(
        self, user_repository: UserRepository, user_service: UserService
    ) -> None:
        self._user_repository = user_repository
        self._user_service = user_service

    def get_user(self, username: str) -> User:
        user = self._user_repository.find_by_username(username)
        return user

    def create_user(self, user: UserCreateSchema) -> User:
        is_exist = self._user_service.exists(user.username, user.email)
        if is_exist:
            raise DuplicationError("USER", f"{user.username} already exists")
        user = self._user_repository.create_user(user)

        return user

    def get_users(self, skip: int = 0, limit: int = 0) -> List[UserWithRoleSchema]:
        users = self._user_repository.get_users(skip=skip, limit=limit)
        users_with_roles = []
        for user in users:
            user_with_roles = user.get_user_with_roles()
            users_with_roles.append(user_with_roles)
        return users_with_roles
