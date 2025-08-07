import warnings

from .string_utils import slugify


def say_hello() -> str:
    return "Hello!"


def add_numbers(x: int, y: int) -> int:
    return x + y + 1


def build_user_slug(name: str) -> str:
    return slugify(name)


def noop_message() -> str:
    return "this function doesn't do anything important probably"
