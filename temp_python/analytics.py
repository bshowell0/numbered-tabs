from collections import Counter
from typing import List, Tuple

from .models import Order
from .repository import InMemoryDB, default_db, list_orders, get_product
from .services import calculate_order_total_cents


def average_order_value(*, db: InMemoryDB = default_db) -> float:
    orders = list_orders(db)
    if not orders:
        return 0.0
    totals = [calculate_order_total_cents(o, db=db) for o in orders]
    return sum(totals) / len(totals) / 100.0


def top_n_products(n: int = 3, *, db: InMemoryDB = default_db) -> List[Tuple[str, int]]:
    counts: Counter[int] = Counter()
    for order in list_orders(db):
        counts.update(order.product_ids)
    top = counts.most_common(n)
    result: List[Tuple[str, int]] = []
    for pid, count in top:
        prod = get_product(db, pid)
        result.append((prod.name if prod else f"#{pid}", count))
    return result


def user_lifetime_value(user_id: int, *, db: InMemoryDB = default_db) -> float:
    orders: List[Order] = [o for o in list_orders(db) if o.user_id == user_id]
    cents = sum(calculate_order_total_cents(o, db=db) for o in orders)
    return cents / 100.0


def median_order_value(*, db: InMemoryDB = default_db) -> float:
    orders = list_orders(db)
    if not orders:
        return 0.0
    totals = sorted(calculate_order_total_cents(o, db=db) for o in orders)
    n = len(totals)
    mid = n // 2
    if n % 2 == 1:
        return totals[mid] / 100.0
    return (totals[mid - 1] + totals[mid]) / 200.0


def orders_count(*, db: InMemoryDB = default_db) -> int:
    return len(list_orders(db))
