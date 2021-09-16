from contextlib import AbstractContextManager
from typing import Callable, Dict, Generator, Tuple

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
from tests.utils.user import get_admin_token_headers

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
    with app.container.db.override(  # type: ignore
        providers.Singleton(Database, db_url=SQLALCEMY_TEST_DATABASE_URL)
    ):
        yield TestClient(app)


@pytest.fixture(scope="module")
def create_root_and_guest_user() -> None:
    """
    APIのテスト用。AdminとGuestロールのユーザを作成する。
    """
    container = Container()
    db = container.db_provider()
    db.create_database()
    session_factory = db.session

    user = User(
        "john", "john@example.com", "ジョン", User.get_hashed_password("plain"), "system"
    )
    admin_role = Role("Admin", "")
    guest_role = Role("Admin", "")
    user_role = UserRole(user.username, admin_role.id)

    guest_user = User(
        "emma", "emma@example.com", "エマ", User.get_hashed_password("dummy"), "system"
    )

    with session_factory() as session:
        session.query(User).delete()
        session.query(Role).delete()
        session.query(UserRole).delete()
        session.add(user)
        session.add(guest_user)
        session.add(admin_role)
        session.add(guest_role)
        session.add(user_role)
        session.commit()
        session.refresh(user)
        session.refresh(guest_user)
        session.refresh(admin_role)
        session.refresh(guest_role)
        session.refresh(user_role)


@pytest.fixture(scope="module")
def admin_token_headers(client: TestClient) -> Dict[str, str]:
    return get_admin_token_headers(client=client)
