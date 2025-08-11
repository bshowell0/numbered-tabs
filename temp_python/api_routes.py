from typing import Dict, List, Optional, Any
import json

from .models import User, Product, Order
from .services import (
    create_new_user,
    get_user,
    get_active_users,
    search_users,
    deactivate_user,
    add_sample_product,
    place_order,
    calculate_order_total_cents,
)
from .analytics import average_order_value, user_lifetime_value, total_revenue_cents
from .repository import default_db, get_product, list_orders
from .validators import validate_email


# Mock request/response objects for realistic API structure
class MockRequest:
    def __init__(self, json_data: Dict[str, Any], args: Dict[str, str] = None):
        self.json = json_data
        self.args = args or {}


class MockResponse:
    def __init__(self, data: Any, status_code: int = 200):
        self.data = data
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        return {"data": self.data, "status": self.status_code}


# User endpoints


def create_user_endpoint(request: MockRequest) -> MockResponse:
    """POST /api/users"""
    try:
        email = request.json.get("email")
        name = request.json.get("name")

        if not email or not validate_email(email):
            return MockResponse({"error": "Invalid email"}, 400)
        if not name:
            return MockResponse({"error": "Name is required"}, 400)

        user = create_new_user(email, name)
        return MockResponse(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "active": user.active,
            },
            201,
        )
    except Exception as e:
        return MockResponse({"error": str(e)}, 500)


def get_user_endpoint(user_id: int) -> MockResponse:
    """GET /api/users/{user_id}"""
    user = get_user(user_id)
    if not user:
        return MockResponse({"error": "User not found"}, 404)

    return MockResponse(
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "active": user.active,
            "display_name": user.display_name(),
        }
    )


def list_users_endpoint(request: MockRequest) -> MockResponse:
    """GET /api/users"""
    search_query = request.args.get("q")

    if search_query:
        users = search_users(search_query)
    else:
        users = get_active_users()

    return MockResponse(
        [
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "active": user.active,
            }
            for user in users
        ]
    )


def deactivate_user_endpoint(user_id: int) -> MockResponse:
    """DELETE /api/users/{user_id}"""
    success = deactivate_user(user_id)
    if not success:
        return MockResponse({"error": "User not found"}, 404)

    return MockResponse({"message": "User deactivated"})


# Product endpoints


def create_product_endpoint(request: MockRequest) -> MockResponse:
    """POST /api/products"""
    try:
        name = request.json.get("name")
        price = request.json.get("price_cents")

        if not name:
            return MockResponse({"error": "Product name is required"}, 400)
        if not isinstance(price, int) or price <= 0:
            return MockResponse({"error": "Valid price is required"}, 400)

        product = add_sample_product(name, price)
        return MockResponse(
            {
                "id": product.id,
                "name": product.name,
                "price_cents": product.price_cents,
            },
            201,
        )
    except Exception as e:
        return MockResponse({"error": str(e)}, 500)


def get_product_endpoint(product_id: int) -> MockResponse:
    """GET /api/products/{product_id}"""
    product = get_product(default_db, product_id)
    if not product:
        return MockResponse({"error": "Product not found"}, 404)

    return MockResponse(
        {
            "id": product.id,
            "name": product.name,
            "price_cents": product.price_cents,
            "price_dollars": product.price_cents / 100.0,
        }
    )


# Order endpoints


def create_order_endpoint(request: MockRequest) -> MockResponse:
    """POST /api/orders"""
    try:
        user_id = request.json.get("user_id")
        product_ids = request.json.get("product_ids", [])
        notes = request.json.get("notes", "")

        if not user_id:
            return MockResponse({"error": "User ID is required"}, 400)
        if not product_ids:
            return MockResponse({"error": "At least one product is required"}, 400)

        order = place_order(user_id, product_ids)
        order.notes = notes

        total_cents = calculate_order_total_cents(order)

        return MockResponse(
            {
                "id": order.id,
                "user_id": order.user_id,
                "product_ids": order.product_ids,
                "notes": order.notes,
                "total_cents": total_cents,
                "total_dollars": total_cents / 100.0,
            },
            201,
        )
    except ValueError as e:
        return MockResponse({"error": str(e)}, 400)
    except Exception as e:
        return MockResponse({"error": str(e)}, 500)


def list_orders_endpoint(request: MockRequest) -> MockResponse:
    """GET /api/orders"""
    user_id_filter = request.args.get("user_id")
    orders = list_orders(default_db)

    if user_id_filter:
        try:
            user_id = int(user_id_filter)
            orders = [o for o in orders if o.user_id == user_id]
        except ValueError:
            return MockResponse({"error": "Invalid user_id parameter"}, 400)

    return MockResponse(
        [
            {
                "id": order.id,
                "user_id": order.user_id,
                "product_ids": order.product_ids,
                "notes": order.notes,
                "total_cents": calculate_order_total_cents(order),
            }
            for order in orders
        ]
    )


# Analytics endpoints


def analytics_overview_endpoint() -> MockResponse:
    """GET /api/analytics/overview"""
    return MockResponse(
        {
            "average_order_value": average_order_value(),
            "total_revenue_cents": total_revenue_cents(),
            "total_revenue_dollars": total_revenue_cents() / 100.0,
            "active_users_count": len(get_active_users()),
            "total_orders_count": len(list_orders(default_db)),
        }
    )


def user_analytics_endpoint(user_id: int) -> MockResponse:
    """GET /api/analytics/users/{user_id}"""
    user = get_user(user_id)
    if not user:
        return MockResponse({"error": "User not found"}, 404)

    ltv = user_lifetime_value(user_id)
    user_orders = [o for o in list_orders(default_db) if o.user_id == user_id]

    return MockResponse(
        {
            "user_id": user_id,
            "lifetime_value": ltv,
            "orders_count": len(user_orders),
            "average_order_value": ltv / len(user_orders) if user_orders else 0.0,
        }
    )


# Health check


def health_check_endpoint() -> MockResponse:
    """GET /api/health"""
    return MockResponse(
        {"status": "healthy", "service": "temp_python_api", "version": "0.1.0"}
    )


# Route mapping (for reference)
ROUTES = {
    "POST /api/users": create_user_endpoint,
    "GET /api/users/{id}": get_user_endpoint,
    "GET /api/users": list_users_endpoint,
    "DELETE /api/users/{id}": deactivate_user_endpoint,
    "POST /api/products": create_product_endpoint,
    "GET /api/products/{id}": get_product_endpoint,
    "POST /api/orders": create_order_endpoint,
    "GET /api/orders": list_orders_endpoint,
    "GET /api/analytics/overview": analytics_overview_endpoint,
    "GET /api/analytics/users/{id}": user_analytics_endpoint,
    "GET /api/health": health_check_endpoint,
}
