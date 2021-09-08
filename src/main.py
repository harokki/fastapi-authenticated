from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def fake_decoded_token(token: str):
    return User(
        username=token + "fakedecoded", email="harokki@example.com", full_name="harokki"
    )


async def get_current_user(token: str = Depends((oauth2_schema))):  # noqa: B008
    user = fake_decoded_token(token)
    return user


@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):  # noqa: B008
    return current_user
