from typing import Union

from app.api_schema import UserInDB
from app.domains.repositories.user_repository import UserRepository

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


class SAUserRepository(UserRepository):
    def find_by_username(self, username: str) -> Union[UserInDB, None]:
        if username in fake_users_db:
            user_dict = fake_users_db[username]
            return UserInDB(**user_dict)
        return None
