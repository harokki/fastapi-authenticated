from typing import Dict

from fastapi.testclient import TestClient


def get_admin_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {"username": "john", "password": "plain"}
    r = client.post("/token", data=login_data)
    tokens = r.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
