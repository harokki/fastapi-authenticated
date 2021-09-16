from fastapi import FastAPI

from .api import deps
from .api.routers import login, users
from .containers import Container


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[login, users, deps])

    app = FastAPI()
    app.container = container  # type: ignore
    app.include_router(login.router)
    app.include_router(users.router)
    return app


app = create_app()
