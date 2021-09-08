from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.api_schema import Token
from app.containers import Container
from app.services.login_service import LoginService

router = APIRouter()

hashed = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": hashed,
        "disabled": False,
    }
}

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/")
async def read_root(token: str = Depends(oauth2_schema)):
    return {"token": token}


@router.post("/token", response_model=Token)
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_service: LoginService = Depends(Provide[Container.login_service]),
):
    user = login_service.authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = login_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
