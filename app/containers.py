from dependency_injector import containers, providers

from app.services.login_service import LoginService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    login_service = providers.Factory(LoginService)
