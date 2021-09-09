from dependency_injector import containers, providers

from app.infrastructures.repositories.user_repository import SAUserRepository
from app.services.login_service import LoginService
from app.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    user_repository = providers.Factory(SAUserRepository)

    login_service = providers.Factory(LoginService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
