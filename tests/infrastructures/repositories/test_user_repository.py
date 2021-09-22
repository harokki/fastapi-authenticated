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
        "password": "plainplain",
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
    assert got_user.hashed_password != "plainplain"
    assert got_user.created_by == "john"
    assert got_user.created_at
    assert got_user.updated_by == "john"
    assert got_user.updated_at


def test_get_users(db: DbFixtureType):
    repositories, session_factory = db
    user_repository = repositories.user_repository

    user1 = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="plainplain",
        created_by="john",
    )
    user2 = User(
        username="anny",
        email="anny@example.com",
        account_name="アニー",
        hashed_password="plainplain",
        created_by="john",
    )

    with session_factory() as session:
        session.add(user1)
        session.add(user2)
        session.commit()
        session.refresh(user1)
        session.refresh(user2)
    got_user = user_repository.get_users()

    got_user1 = got_user[0]
    got_user2 = got_user[1]
    assert len(got_user) == 2
    assert got_user1.username == "john"
    assert got_user1.email == "john@example.com"
    assert got_user1.account_name == "ジョン"
    assert got_user1.is_active is True
    assert got_user1.hashed_password == "plainplain"
    assert got_user1.created_by == "john"
    assert got_user1.created_at
    assert got_user1.updated_by == "john"
    assert got_user1.updated_at

    assert got_user2.username == "anny"
    assert got_user2.email == "anny@example.com"
    assert got_user2.account_name == "アニー"
    assert got_user2.is_active is True
    assert got_user2.hashed_password == "plainplain"
    assert got_user2.created_by == "john"
    assert got_user2.created_at
    assert got_user2.updated_by == "john"
    assert got_user2.updated_at


def test_get_users_with_skip_limit(db: DbFixtureType):
    repositories, session_factory = db
    user_repository = repositories.user_repository

    user1 = User(
        username="john",
        email="john@example.com",
        account_name="ジョン",
        hashed_password="plainplain",
        created_by="john",
    )
    user2 = User(
        username="anny",
        email="anny@example.com",
        account_name="アニー",
        hashed_password="plainplain",
        created_by="john",
    )
    user3 = User(
        username="James",
        email="james@example.com",
        account_name="ジェームズ",
        hashed_password="plainplain",
        created_by="john",
    )

    with session_factory() as session:
        session.add(user1)
        session.add(user2)
        session.add(user3)
        session.commit()
        session.refresh(user1)
        session.refresh(user2)
        session.refresh(user3)
    got_user = user_repository.get_users(skip=1, limit=1)

    got_user1 = got_user[0]
    assert len(got_user) == 1
    assert got_user1.username == "anny"
    assert got_user1.email == "anny@example.com"
    assert got_user1.account_name == "アニー"
    assert got_user1.is_active is True
    assert got_user1.hashed_password == "plainplain"
    assert got_user1.created_by == "john"
    assert got_user1.created_at
    assert got_user1.updated_by == "john"
    assert got_user1.updated_at
