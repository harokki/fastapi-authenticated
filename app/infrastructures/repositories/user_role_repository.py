from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.domains.entities.user_role import UserRole
from app.domains.repositories.user_role_repository import UserRoleRepository
from app.schemas.user import UserRoleSchema


class SAUserRoleRepository(UserRoleRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def create_user_role(self, user_role: UserRoleSchema) -> UserRole:
        with self.session_factory() as session:
            db_user_role = UserRole(**user_role.dict())
            session.add(db_user_role)
            session.commit()
            session.refresh(db_user_role)
        return db_user_role
