from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.applications.login_service import LoginApplicationService
from app.containers import Container
from app.schemas.token import Token

router = APIRouter()


@router.post("/token", response_model=Token)
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_service: LoginApplicationService = Depends(
        Provide[Container.login_application_service]
    ),
):
    user = login_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    role_names = user.get_role_names()
    if not role_names:
        role_names.append("Guest")
    access_token = login_service.create_access_token(
        data={"sub": user.username, "scopes": role_names}
    )
    return {"access_token": access_token, "token_type": "bearer"}
