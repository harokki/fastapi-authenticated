from dependency_injector import providers
from fastapi.testclient import TestClient

from app.database import Database
from app.main import app
from tests.conftest import SQLALCEMY_TEST_DATABASE_URL


def test_get_access_token(client: TestClient, create_root_user):
    login_data = {"username": "john", "password": "plain"}

    with app.container.db.override(  # type: ignore
        providers.Singleton(Database, db_url=SQLALCEMY_TEST_DATABASE_URL)
    ):
        r = client.post("/token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
