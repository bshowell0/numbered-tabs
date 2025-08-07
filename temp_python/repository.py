from typing import Dict, List, Optional

from .models import Order, Product, User


class InMemoryDB:
    def __init__(self) -> None:
        self.users: Dict[int, User] = {}
        self.products: Dict[int, Product] = {}
        self.orders: Dict[int, Order] = {}
        self._next_user_id = 1
        self._next_product_id = 1
        self._next_order_id = 1

    def generate_user_id(self) -> int:
        uid = self._next_user_id
        self._next_user_id += 1
        return uid

    def generate_product_id(self) -> int:
        pid = self._next_product_id
        self._next_product_id += 1
        return pid

    def generate_order_id(self) -> int:
        oid = self._next_order_id
        self._next_order_id += 1
        return oid


default_db = InMemoryDB()


# User operations


def add_user(db: InMemoryDB, user: User) -> User:
    db.users[user.id] = user
    return user


def get_user(db: InMemoryDB, user_id: int) -> Optional[User]:
    return db.users.get(user_id)


def list_users(db: InMemoryDB) -> List[User]:
    return list(db.users.values())


def find_users_by_name(db: InMemoryDB, query: str) -> List[User]:
    q = query.lower()
    return [u for u in db.users.values() if q in u.name.lower()]


def deactivate_user(db: InMemoryDB, user_id: int) -> bool:
    user = db.users.get(user_id)
    if not user:
        return False
    user.active = False
    return True


# Product operations


def add_product(db: InMemoryDB, product: Product) -> Product:
    db.products[product.id] = product
    return product


def get_product(db: InMemoryDB, product_id: int) -> Optional[Product]:
    return db.products.get(product_id)


def list_products(db: InMemoryDB) -> List[Product]:
    return list(db.products.values())


# Order operations


def add_order(db: InMemoryDB, order: Order) -> Order:
    db.orders[order.id] = order
    return order


def get_order(db: InMemoryDB, order_id: int) -> Optional[Order]:
    return db.orders.get(order_id)


def list_orders(db: InMemoryDB) -> List[Order]:
    return list(db.orders.values())
