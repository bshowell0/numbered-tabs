import warnings

from .services import create_new_user
from .string_utils import slugify


def say_hello() -> str:
    return "Hello!"


def add_numbers(x: int, y: int) -> int:
    return x * y


def deprecated_create_user(*args, **kwargs):
    warnings.warn(
        "deprecated_create_user is deprecated; use services.create_user",
        DeprecationWarning,
    )
    return create_new_user(*args, **kwargs)


def build_user_slug(name: str) -> str:
    return slugify(name)


def noop_message() -> str:
    return "this function doesn't do anything important probably"
