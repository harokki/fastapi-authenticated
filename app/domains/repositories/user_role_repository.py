from abc import ABCMeta, abstractmethod

from app.domains.entities.user_role import UserRole
from app.schemas.user import UserRoleSchema


class UserRoleRepository(metaclass=ABCMeta):
    @abstractmethod
    def create_user_role(self, user_role: UserRoleSchema) -> UserRole:
        raise NotImplementedError
