from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError

from app.api_schema import TokenData, UserSchema
from app.applications import ALGORITHM, SECRET_KEY
from app.applications.user_service import UserApplicationService
from app.containers import Container
from app.domains.entities.user import User
from app.routers import oauth2_schema

router = APIRouter()


@inject
async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_schema),
    user_service: UserApplicationService = Depends(Provide[Container.user_service]),
) -> User:
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope={security_scopes.scope_str}"
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = user_service.get_user(token_data.username if token_data.username else "")
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=[])
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/users/me", response_model=UserSchema)
@inject
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
