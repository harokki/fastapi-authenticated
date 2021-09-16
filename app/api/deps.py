from fastapi.security import OAuth2PasswordBearer

from app.domains.constants.role import Role

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        Role.Guest["name"]: Role.Guest["description"],
        Role.Admin["name"]: Role.Admin["description"],
    },
)
