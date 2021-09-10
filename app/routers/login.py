from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api_schema import Token
from app.applications.login_service import LoginApplicationService
from app.containers import Container
from app.routers import oauth2_schema

router = APIRouter()


@router.get("/")
async def read_root(token: str = Depends(oauth2_schema)):
    return {"token": token}


@router.post("/token", response_model=Token)
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_service: LoginApplicationService = Depends(Provide[Container.login_service]),
):
    user = login_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = login_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
