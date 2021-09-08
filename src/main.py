from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def read_root(token: str = Depends(oauth2_schema)):  # noqa: B008
    return {"token": token}
