from app.domains.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def exists(self, username: str, email: str) -> bool:
        found_user_by_username = self._user_repository.find_by_username(username)
        found_user_by_email = self._user_repository.find_by_email(email)

        if found_user_by_username or found_user_by_email:
            return True
        return False
