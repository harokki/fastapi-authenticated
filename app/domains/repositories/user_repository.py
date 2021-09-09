from abc import ABCMeta, abstractmethod
from typing import Union

from app.api_schema import UserInDB


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_username(self, username: str) -> Union[UserInDB, None]:
        raise NotImplementedError
