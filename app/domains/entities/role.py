from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import validates

from app.database import Base
from app.domains.validations import check_length


class Role(Base):
    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(256), nullable=False)

    def __init__(self, name: str, description: str) -> None:
        self.id = str(uuid4())
        self.name = name
        self.description = description

    @validates("name")
    def validate_name(self, _, value) -> str:
        check_length(value, 1, 100)
        return value

    @validates("description")
    def validate_description(self, _, value) -> str:
        check_length(value, 0, 256)
        return value
