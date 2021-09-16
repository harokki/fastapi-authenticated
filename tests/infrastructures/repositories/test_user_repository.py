from app.domains.entities.role import Role
from app.domains.entities.user import User
from app.domains.entities.user_role import UserRole
from app.schemas.user import UserCreateSchema
from tests.conftest import DbFixtureType

SQLALCEMY_DATABASE_URL = "sqlite:///./test.db"


def test_find_by_user_id(db: DbFixtureType):
    repositories, session_factory = db
    user_repository = repositories.user_repository

    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="aaaaa",
        created_by="john",
    )

    with session_factory() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    got_user = user_repository.find_by_username("john")

    assert got_user.username == "john"
    assert got_user.email == "john@example.com"
    assert got_user.account_name == "ジョン"
    assert got_user.is_active is True
    assert got_user.hashed_password == "aaaaa"
    assert got_user.created_by == "john"
    assert got_user.created_at
    assert got_user.updated_by == "john"
    assert got_user.updated_at


def test_find_by_email(db: DbFixtureType):
    repositories, session_factory = db
    user_repository = repositories.user_repository

    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="aaaaa",
        created_by="john",
    )

    with session_factory() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    got_user = user_repository.find_by_email("john@example.com")

    assert got_user.username == "john"
    assert got_user.email == "john@example.com"
    assert got_user.account_name == "ジョン"
    assert got_user.is_active is True
    assert got_user.hashed_password == "aaaaa"
    assert got_user.created_by == "john"
    assert got_user.created_at
    assert got_user.updated_by == "john"
    assert got_user.updated_at


def test_get_user_role(db: DbFixtureType):
    repositories, session_factory = db
    user_repository = repositories.user_repository

    user = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="aaaaa",
        created_by="john",
    )

    role = Role("Admin", "")
    super_role = Role("Super Admin", "")

    user_role = UserRole(user.username, role.id)
    user_role_2 = UserRole(user.username, super_role.id)

    with session_factory() as session:
        session.add(user)
        session.add(role)
        session.add(super_role)
        session.add(user_role)
        session.add(user_role_2)
        session.commit()
        session.refresh(user)
        session.refresh(role)
        session.refresh(super_role)
        session.refresh(user_role)
        session.refresh(user_role_2)
    got_user = user_repository.find_by_username("john")

    assert len(got_user.user_role) == 2
    assert sorted(got_user.get_role_names()) == sorted(["Admin", "Super Admin"])


def test_create_user(db: DbFixtureType):
    data = {
        "username": "emma",
        "email": "emma@example.com",
        "account_name": "エマ",
        "is_active": "True",
        "password": "plain",
        "created_by": "john",
    }
    user = UserCreateSchema(**data)

    repositories, _ = db
    user_repository = repositories.user_repository

    user_repository.create_user(user)

    got_user = user_repository.find_by_username("emma")

    assert got_user.username == "emma"
    assert got_user.email == "emma@example.com"
    assert got_user.account_name == "エマ"
    assert got_user.is_active is True
    assert got_user.hashed_password != "plain"
    assert got_user.created_by == "john"
    assert got_user.created_at
    assert got_user.updated_by == "john"
    assert got_user.updated_at
