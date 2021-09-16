from contextlib import AbstractContextManager
from typing import Callable, Generator, Tuple

import pytest
from dependency_injector import containers, providers
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import Database
from app.domains.entities.role import Role
from app.domains.entities.user import User
from app.domains.entities.user_role import UserRole
from app.infrastructures.repositories.user_repository import SAUserRepository
from app.infrastructures.repositories.user_role_repository import SAUserRoleRepository
from app.main import app

SQLALCEMY_TEST_DATABASE_URL = "sqlite:///./test.db"


# TODO: 本番用のContainerと二重管理になっているのでなんとかしたい
class Container(containers.DeclarativeContainer):

    db_provider = providers.Singleton(Database, db_url=SQLALCEMY_TEST_DATABASE_URL)

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


@pytest.fixture(scope="module")
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(scope="module")
def create_root_user() -> None:
    """
    APIのテスト用。Adminロールのユーザを作成する。
    """
    container = Container()
    db = container.db_provider()
    db.create_database()
    session_factory = db.session

    user = User(
        "john", "john@example.com", "ジョン", User.get_hashed_password("plain"), "system"
    )
    role = Role("Admin", "")
    user_role = UserRole(user.username, role.id)

    with session_factory() as session:
        session.query(User).delete()
        session.query(Role).delete()
        session.query(UserRole).delete()
        session.add(user)
        session.add(role)
        session.add(user_role)
        session.commit()
        session.refresh(user)
        session.refresh(role)
        session.refresh(user_role)
