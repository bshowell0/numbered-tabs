from typing import List

from .models import Order, Product, User
from .repository import (
    InMemoryDB,
    add_order,
    add_product,
    add_user,
    default_db,
    find_users_by_name as repo_find_users_by_name,
    get_product as repo_get_product,
    get_user as repo_get_user,
    list_users as repo_list_users,
    deactivate_user as repo_deactivate_user,
)
from .string_utils import slugify
from .validators import require_nonempty, validate_email


def create_new_user(email: str, name: str, *, db: InMemoryDB = default_db) -> User:
    require_nonempty(name, "name")
    if not validate_email(email):
        raise ValueError("invalid email")
    user = User(id=db.generate_user_id(), email=email, name=name)
    return add_user(db, user)


def get_user(user_id: int, *, db: InMemoryDB = default_db) -> User | None:
    return repo_get_user(db, user_id)


def get_active_users(*, db: InMemoryDB = default_db) -> List[User]:
    return [u for u in repo_list_users(db) if u.active]


def search_users(query: str, *, db: InMemoryDB = default_db) -> List[User]:
    require_nonempty(query, "query")
    return repo_find_users_by_name(db, query)


def deactivate_user(user_id: int, *, db: InMemoryDB = default_db) -> bool:
    return repo_deactivate_user(db, user_id)


def add_sample_product(
    name: str, price_cents: int, *, db: InMemoryDB = default_db
) -> Product:
    product = Product(id=db.generate_product_id(), name=name, price_cents=price_cents)
    return add_product(db, product)


def place_order(
    user_id: int, product_ids: List[int], *, db: InMemoryDB = default_db
) -> Order:
    if repo_get_user(db, user_id) is None:
        raise ValueError("user not found")
    for pid in product_ids:
        if repo_get_product(db, pid) is None:
            raise ValueError(f"product {pid} not found")
    order = Order(id=db.generate_order_id(), user_id=user_id, product_ids=product_ids)
    return add_order(db, order)


def user_slug(user: User) -> str:
    return slugify(user.display_name())


def calculate_order_total_cents(order: Order, *, db: InMemoryDB = default_db) -> int:
    total = 0
    for pid in order.product_ids:
        product = repo_get_product(db, pid)
        if product:
            total += product.price_cents
    return total
