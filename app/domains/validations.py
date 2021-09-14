from app.domains.exceptions import ValidationError


def check_length(value: str, lower: int, upper: int) -> str:
    if not lower <= len(value) <= upper:
        raise ValidationError(value, f"must be {lower} or more and {upper} or less")
    return value
