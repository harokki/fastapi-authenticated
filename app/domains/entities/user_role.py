from sqlalchemy import Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship, validates

from app.database import Base
from app.domains.validations import check_length


class UserRole(Base):
    __tablename__ = "user_roles"

    username = Column(
        String(32),
        ForeignKey("users.username"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        String(36),
        ForeignKey("roles.id"),
        primary_key=True,
        nullable=False,
    )

    role = relationship("Role", lazy="subquery")
    user = relationship("User", back_populates="user_role", uselist=False)

    __table_args__ = (UniqueConstraint("username", "role_id", name="unique_user_role"),)

    def __init__(self, username: str, role_id: str) -> None:
        self.username = username
        self.role_id = role_id

    @validates("username")
    def validate_username(self, _, value):
        check_length(value, 1, 32)
        return value

    @validates("role_id")
    def validate_role_id(self, _, value):
        check_length(value, 1, 36)
        return value
