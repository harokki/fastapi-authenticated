from sqlalchemy import Boolean, Column, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    account_name = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
