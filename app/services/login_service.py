from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.domains.repositories.user_repository import UserRepository

from . import ALGORITHM, SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def authenticate_user(self, username: str, password: str):
        user = self._user_repository.find_by_username(username)
        if not user:
            return False
        if not self._verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict):
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def _verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str):
        return pwd_context.hash(password)
