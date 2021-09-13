from datetime import datetime, timedelta

from jose import jwt

from app.domains.entities.user import User
from app.domains.exceptions import Error
from app.domains.repositories.user_repository import UserRepository

from . import ALGORITHM, SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginApplicationService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def authenticate_user(self, username: str, password: str) -> User:
        user = self._user_repository.find_by_username(username)
        if not user:
            raise Error("user not found", "NOT_FOUND_ERROR")
        if not user.verify_password(password):
            raise Error("verify password is failed", "AUTHENTICATE_ERROR")
        return user

    def create_access_token(self, data: dict) -> str:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
