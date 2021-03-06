from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.api.deps import get_current_active_user
from app.applications.user_service import UserApplicationService
from app.containers import Container
from app.domains.constants.role import Role
from app.domains.entities.user import User
from app.domains.exceptions import DuplicationError, ValidationError
from app.schemas.user import (
    UserAPICreateSchema,
    UserCreateSchema,
    UserSchema,
    UserWithRoleSchema,
)

router = APIRouter()


@router.get("/users/me", response_model=UserSchema)
@inject
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users", response_model=List[UserWithRoleSchema])
@inject
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserApplicationService = Depends(
        Provide[Container.user_application_service]
    ),
):
    users = user_service.get_users(skip=skip, limit=limit)
    return users


@router.post("/users", response_model=UserSchema)
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
    user_dict["is_active"] = True
    user_dict["created_by"] = current_user.username
    user_with_created_by = UserCreateSchema(**user_dict)
    try:
        created_user = user_service.create_user(user_with_created_by)
    except DuplicationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="username or email already Exists",
        )
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"expression": error.args[0], "message": error.args[1]},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="there was a problem creating the user.",
        )
    return created_user
