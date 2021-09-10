from contextlib import AbstractContextManager
from typing import Callable, Tuple

import pytest
from dependency_injector import containers, providers
from sqlalchemy.orm import Session

from app.database import Database
from app.domains.entities.user import User
from app.infrastructures.repositories.user_repository import SAUserRepository

SQLALCEMY_DATABASE_URL = "sqlite:///./test.db"


class Container(containers.DeclarativeContainer):

    db_provider = providers.Singleton(Database, db_url=SQLALCEMY_DATABASE_URL)
    user_repository = providers.Singleton(
        SAUserRepository, session_factory=db_provider.provided.session
    )


@pytest.fixture
def db() -> Tuple[SAUserRepository, Callable[..., AbstractContextManager[Session]]]:
    container = Container()
    db = container.db_provider()
    user_repository = container.user_repository()
    db.create_database()
    session_factory = db.session

    with session_factory() as session:
        session.query(User).delete()
        session.commit()

    return user_repository, session_factory


def test_find_by_user_id(
    db: Tuple[SAUserRepository, Callable[..., AbstractContextManager[Session]]]
):
    user_repository, session_factory = db

    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="aaaaa",
        created_by="john",
    )

    with session_factory() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        got_user = user_repository.find_by_username("john")

    assert got_user.username == "john"
    assert got_user.email == "john@example.com"
    assert got_user.account_name == "ジョン"
    assert got_user.is_active is True
    assert got_user.hashed_password == "aaaaa"
    assert got_user.created_by == "john"
    assert got_user.created_at
    assert got_user.updated_by == "john"
    assert got_user.updated_at
