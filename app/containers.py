from dependency_injector import containers, providers

from app.applications.login_service import LoginApplicationService
from app.applications.user_service import UserApplicationService
from app.database import Database
from app.infrastructures.repositories.user_repository import SAUserRepository

SQLALCEMY_DATABASE_URL = "sqlite:///./app.db"


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=SQLALCEMY_DATABASE_URL)

    user_repository = providers.Factory(
        SAUserRepository, session_factory=db.provided.session
    )

    login_service = providers.Factory(
        LoginApplicationService, user_repository=user_repository
    )
    user_service = providers.Factory(
        UserApplicationService, user_repository=user_repository
    )
