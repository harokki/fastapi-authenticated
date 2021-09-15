from app.domains.entities.role import Role
from app.domains.entities.user import User
from app.domains.entities.user_role import UserRole
from app.schemas.user import UserRoleSchema
from tests.conftest import DbFixtureType


def test_create_user_role(db: DbFixtureType):
    repositories, session_factory = db
    user_role_repository = repositories.user_role_repository

    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="aaaaa",
        created_by="john",
    )

    role = Role("Admin", "")

    data = UserRoleSchema(**{"username": user.username, "role_id": role.id})

    user_role_repository.create_user_role(data)

    with session_factory() as session:
        user_roles = session.query(UserRole).all()

    assert len(user_roles) == 1
    assert user_roles[0].username == "john"
    assert user_roles[0].role_id == role.id
