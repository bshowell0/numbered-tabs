import re

from .models import User

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email))


def require_nonempty(value: str, field_name: str = "value") -> str:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be non-empty")
    return value


def assert_valid_user(user: User) -> None:
    require_nonempty(user.name, "name")
    if not validate_email(user.email):
        raise ValueError("invalid email")
