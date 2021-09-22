from abc import ABCMeta, abstractmethod
from typing import List

from app.domains.entities.user import User
from app.schemas.user import UserCreateSchema


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, user: UserCreateSchema) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        raise NotImplementedError
