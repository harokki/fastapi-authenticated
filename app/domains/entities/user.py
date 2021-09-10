from datetime import datetime, timezone

from passlib.context import CryptContext
from sqlalchemy import TIMESTAMP, Boolean, Column, String

from app.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    username = Column(String(32), primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    account_name = Column(String(32), index=True, nullable=False)
    hashed_password = Column(String(64), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now, nullable=False)
    created_by = Column(String(32), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now, nullable=False)
    updated_by = Column(String(32), nullable=False)

    def __init__(
        self,
        username: str,
        email: str,
        account_name: str,
        hashed_password: str,
        created_by: str,
    ):
        self.username = username
        self.email = email
        self.account_name = account_name
        self.hashed_password = hashed_password
        self.is_active = True
        self.created_at = datetime.now(timezone.utc)
        self.created_by = created_by
        self.updated_at = self.created_at
        self.updated_by = created_by

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def get_hashed_password(plain_password: str) -> str:
        return pwd_context.hash(plain_password)
