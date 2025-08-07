from typing import Callable, Dict

from .analytics import average_order_value
from .repository import InMemoryDB, default_db
from .services import create_user, list_active_users


def nightly_recompute_metrics(*, db: InMemoryDB = default_db) -> Dict[str, float]:
    return {"average_order_value": average_order_value(db=db)}


def send_welcome_emails(
    send_func: Callable[[str], None], *, db: InMemoryDB = default_db
) -> int:
    count = 0
    for user in list_active_users(db=db):
        send_func(user.email)
        count += 1
    return count


def seed_example_data(*, db: InMemoryDB = default_db) -> None:
    if list_active_users(db=db):
        return
    create_user("alice@example.com", "Alice", db=db)
    create_user("bob@example.com", "Bob", db=db)
