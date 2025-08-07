"""
Lightweight sample package for refactoring practice.
"""

from .services import create_user, place_order, get_active_users
from .analytics import average_order_value

__all__ = [
    "create_user",
    "place_order",
    "get_active_users",
    "average_order_value",
]

__version__ = "0.1.0"


def get_version() -> str:
    return __version__
