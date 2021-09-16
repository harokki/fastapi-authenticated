from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError

from app.api.deps import oauth2_schema
from app.applications import ALGORITHM, SECRET_KEY
from app.applications.user_service import UserApplicationService
from app.containers import Container
from app.domains.constants.role import Role
from app.domains.entities.user import User
from app.domains.exceptions import DuplicationError
from app.schemas.token import TokenData
from app.schemas.user import UserAPICreateSchema, UserCreateSchema, UserSchema

router = APIRouter()


@inject
async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_schema),
    user_service: UserApplicationService = Depends(
        Provide[Container.user_application_service]
    ),
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


@router.post("/users/", response_model=UserSchema)
@inject
async def create_user(
    user: UserAPICreateSchema,
    user_service: UserApplicationService = Depends(
        Provide[Container.user_application_service]
    ),
    current_user: User = Security(
        get_current_active_user,
        scopes=[Role.Admin["name"]],
    ),
):
    user_dict = user.dict()
    user_dict["created_by"] = current_user.username
    user_with_created_by = UserCreateSchema(**user_dict)
    try:
        created_user = user_service.create_user(user_with_created_by)
    except DuplicationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="username or email already Exists",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="there was a problem creating the user.",
        )
    return created_user
