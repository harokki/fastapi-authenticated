class Error(Exception):
    pass


class ValidationError(Error):
    def __init__(
        self, expression: str, message: str, code: str = "VALIDATION_ERROR"
    ) -> None:
        self.expression = expression
        self.message = message
        self.code = code
