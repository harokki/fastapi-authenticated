import re
from datetime import datetime, timezone

from passlib.context import CryptContext
from sqlalchemy import TIMESTAMP, Boolean, Column, String
from sqlalchemy.orm import validates

from app.database import Base
from app.domains.exceptions import ValidationError

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

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.username!r}, {self.email!r}, "
            f"{self.account_name!r}, {self.is_active!r})"
        )

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def get_hashed_password(plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    # TODO: いろんなところで使うと思うので別ファイルに切り出す
    def _check_length(self, value: str, lower: int, upper: int) -> str:
        if not lower <= len(value) <= upper:
            raise ValidationError(value, f"must be {lower} or more and {upper} or less")
        return value

    @validates("username")
    def validate_username(self, _, value):
        if re.compile("[a-zA-Z0-9-_]*").fullmatch(value) is None:
            raise ValidationError(
                value, "only alphanumeric, underscore and hyphen is ok"
            )
        self._check_length(value, 1, 32)
        return value

    @validates("email")
    def validate_email(self, _, value):
        if (
            re.compile("[a-zA-Z0-9-._]+@[a-zA-Z0-9-._]+.[A-Za-z]+").fullmatch(value)
            is None
        ):
            raise ValidationError(value, "illegal email format")
        self._check_length(value, 1, 256)
        return value

    @validates("account_name")
    def validate_account_name(self, _, value):
        self._check_length(value, 1, 32)
        return value

    @validates("hashed_password")
    def validate_hashed_password(self, _, value):
        self._check_length(value, 1, 64)
        return value

    @validates("created_by")
    def validate_created_by(self, _, value):
        self._check_length(value, 1, 32)
        return value
