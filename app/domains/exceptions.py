class Error(Exception):
    def __init__(self, message: str, code: str = "ERROR") -> None:
        self.message = message
        self.code = code


class ValidationError(Error):
    def __init__(
        self, expression: str, message: str, code: str = "VALIDATION_ERROR"
    ) -> None:
        super().__init__(message, code)
        self.expression = expression


class NotFoundError(Error):
    def __init__(self, message: str, code: str = "NOTFOUND_ERROR") -> None:
        super().__init__(message, code=code)
