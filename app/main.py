from fastapi import FastAPI

from .containers import Container
from .routers import users


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[users])

    app = FastAPI()
    app.container = container  # type: ignore
    app.include_router(users.router)
    return app


app = create_app()


# oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# async def get_current_user(token: str = Depends(oauth2_schema)) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(
#         fake_users_db, username=token_data.username if token_data.username else ""
#     )
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.get("/users/me")
# async def read_users_me(
#     current_user: User = Depends(get_current_active_user),
# ):
#     return current_user
