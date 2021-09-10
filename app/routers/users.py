from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt

from app.api_schema import TokenData, UserSchema
from app.applications import ALGORITHM, SECRET_KEY
from app.applications.user_service import UserService
from app.containers import Container
from app.domains.entities.user import User
from app.routers import oauth2_schema

router = APIRouter()


@inject
async def get_current_user(
    token: str = Depends(oauth2_schema),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = user_service.get_user(token_data.username if token_data.username else "")
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/users/me", response_model=UserSchema)
@inject
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
