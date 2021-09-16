from typing import Literal

ErrorCode = Literal[
    "ERROR",
    "VALIDATION_ERROR",
    "NOT_FOUND_ERROR",
    "AUTHENTICATE_ERROR",
    "DUPLICATION_ERROR",
]


class Error(Exception):
    def __init__(self, message: str, code: ErrorCode = "ERROR") -> None:
        self.message = message
        self.code = code


class ValidationError(Error):
    def __init__(
        self, expression: str, message: str, code: ErrorCode = "VALIDATION_ERROR"
    ) -> None:
        super().__init__(message, code)
        self.expression = expression


class DuplicationError(Error):
    def __init__(
        self, location: str, message: str, code: ErrorCode = "DUPLICATION_ERROR"
    ) -> None:
        super().__init__(message, code=code)
        self.location = location
