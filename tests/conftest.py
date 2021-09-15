from contextlib import AbstractContextManager
from typing import Callable, Tuple

import pytest
from dependency_injector import containers, providers
from sqlalchemy.orm import Session

from app.database import Database
from app.domains.entities.role import Role
from app.domains.entities.user import User
from app.domains.entities.user_role import UserRole
from app.infrastructures.repositories.user_repository import SAUserRepository
from app.infrastructures.repositories.user_role_repository import SAUserRoleRepository

SQLALCEMY_DATABASE_URL = "sqlite:///./test.db"


class Container(containers.DeclarativeContainer):

    db_provider = providers.Singleton(Database, db_url=SQLALCEMY_DATABASE_URL)
    user_repository = providers.Singleton(
        SAUserRepository, session_factory=db_provider.provided.session
    )
    user_role_repository = providers.Singleton(
        SAUserRoleRepository, session_factory=db_provider.provided.session
    )


class Repositories:
    user_repository: SAUserRepository
    user_role_repository: SAUserRoleRepository

    def __init__(self, user_repository, user_role_repository) -> None:
        self.user_repository = user_repository
        self.user_role_repository = user_role_repository


DbFixtureType = Tuple[Repositories, Callable[..., AbstractContextManager[Session]]]


@pytest.fixture
def db() -> DbFixtureType:
    container = Container()
    db = container.db_provider()
    repositories = Repositories(
        container.user_repository(), container.user_role_repository()
    )
    db.create_database()
    session_factory = db.session

    with session_factory() as session:
        session.query(User).delete()
        session.query(Role).delete()
        session.query(UserRole).delete()
        session.commit()

    return repositories, session_factory
