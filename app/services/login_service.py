from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.api_schema import UserInDB

SECRET_KEY = "a5dc7fa8032d49f8152d39b58ef38807b3364dfa69b40c697716bfc214b50db7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginService:
    def __init__(self) -> None:
        self._repository = "dummy"

    def authenticate_user(self, fake_db, username: str, password: str):
        user = self._get_user(fake_db, username)
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

    # TODO: infrastructuresに移動
    def _get_user(self, db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)

    def _verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str):
        return pwd_context.hash(password)
