from app.domains.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def exists(self, username: str) -> bool:
        user = self._user_repository.find_by_username(username)

        if user:
            return True
        return False
