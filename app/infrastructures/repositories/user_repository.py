from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy.orm import Session

from app.domains.entities.user import User
from app.domains.repositories.user_repository import UserRepository
from app.schemas.user import UserCreateSchema


class SAUserRepository(UserRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def find_by_username(self, username: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.username == username).first()
        return user

    def find_by_email(self, email: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
        return user

    def create_user(self, user: UserCreateSchema) -> User:
        hashed_password = User.get_hashed_password(user.password)
        db_user = User(
            user.username,
            user.email,
            user.account_name,
            hashed_password,
            user.created_by,
        )

        with self.session_factory() as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)

        return db_user

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        with self.session_factory() as session:
            users = session.query(User).offset(skip).limit(limit).all()
        return users
