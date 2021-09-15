from abc import ABCMeta, abstractmethod

from app.domains.entities.user import User
from app.schemas.user import UserCreateSchema


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, user: UserCreateSchema) -> User:
        raise NotImplementedError
