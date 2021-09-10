from abc import ABCMeta, abstractmethod

from app.domains.entities.user import User


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_username(self, username: str) -> User:
        raise NotImplementedError
