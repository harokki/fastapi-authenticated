from fastapi import FastAPI

from .containers import Container
from .routers import login, users


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[login, users])

    app = FastAPI()
    app.container = container  # type: ignore
    app.include_router(login.router)
    app.include_router(users.router)
    return app


app = create_app()
