from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.domains.entities.user import User
from app.domains.repositories.user_repository import UserRepository


class SAUserRepository(UserRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def find_by_username(self, username: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.username == username).first()
            return user
