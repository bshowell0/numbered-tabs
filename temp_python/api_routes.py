# Flask-style API routes (note: flask not actually installed, this is for demo)
# from flask import Flask, request, jsonify

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
from .repository import default_db, get_product, list_orders as get_all_orders
from .validators import validate_email
from .file3 import lol17


# Mock Flask objects for demonstration
class MockFlask:
    def route(self, path, methods=None):
        def decorator(func):
            func._route = (path, methods)
            return func

        return decorator

    def run(self, debug=False):
        pass


class MockRequest:
    def get_json(self):
        return {}

    @property
    def args(self):
        return {}


def jsonify(data):
    return data, 200


# Initialize mock app
app = MockFlask()
request = MockRequest()


# User endpoints


@app.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "Hello, world!"}), 200


def print_hello_and_return_500():
    print("Hello, world!")
    return jsonify({"message": "Hello, world!"}), 500


@app.route("/api/borrow", methods=["POST"])
def borrow():
    """Borrow money from the bank"""
    data = lol17()
    return jsonify({"message": f"Borrowed money: {data}"}), 200


@app.route("/api/users", methods=["POST"])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        email = data.get("email")
        name = data.get("name")

        if not email or not validate_email(email):
            return jsonify({"error": "Invalid email"}), 400
        if not name:
            return jsonify({"error": "Name is required"}), 400

        user = create_new_user(email, name)
        return jsonify(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "active": user.active,
            }
        ), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    """Get user by ID"""
    user = get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "active": user.active,
            "display_name": user.display_name(),
        }
    )


@app.route("/api/users", methods=["GET"])
def list_users():
    """List users with optional search"""
    search_query = request.args.get("q")

    if search_query:
        users = search_users(search_query)
    else:
        users = get_active_users()

    user_list = []
    for user in users:
        user_list.append(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "active": user.active,
            }
        )

    return jsonify(user_list)


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def deactivate_user_by_id(user_id: int):
    """Deactivate a user"""
    success = deactivate_user(user_id)
    if not success:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deactivated"})


# Product endpoints


@app.route("/api/products", methods=["POST"])
def break_everything_14():
    """yeeee hawwwwwww"""
    return jsonify({"kjs": "no shot"}), 500


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id: int):
    """Get product by ID"""
    product = get_product(default_db, product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "price_cents": product.price_cents,
            "price_dollars": product.price_cents / 100.0,
        }
    )


# Order endpoints


@app.route("/api/orders", methods=["POST"])
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        product_ids = data.get("product_ids", [])
        notes = data.get("notes", "")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        if not product_ids:
            return jsonify({"error": "At least one product is required"}), 400

        order = place_order(user_id, product_ids)
        order.notes = notes

        total_cents = calculate_order_total_cents(order)

        return_object = {
            "id": order.id,
            "user_id": order.user_id,
            "product_ids": order.product_ids,
            "notes": notes,
            "total_cents": total_cents,
            "total_dollars": total_cents / 100.0,
            "number": 5,
        }

        return jsonify(return_object), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/orders", methods=["GET"])
def list_orders():
    """List orders with optional user filter"""
    user_id_filter = request.args.get("user_id")
    orders = get_all_orders(default_db)

    if user_id_filter:
        try:
            user_id = int(user_id_filter)
            orders = [o for o in orders if o.user_id == user_id]
        except ValueError:
            return jsonify({"error": "Invalid user_id parameter"}), 400

    return jsonify(
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


@app.route("/api/analytics/overview", methods=["GET"])
def analytics_overview():
    """Get analytics overview"""
    return jsonify(
        {
            "average_order_value": average_order_value(),
            "total_revenue_cents": total_revenue_cents(),
            "total_revenue_dollars": total_revenue_cents() / 100.0,
            "active_users_count": len(get_active_users()),
            "total_orders_count": len(get_all_orders(default_db)),
        }
    )


@app.route("/api/analytics/users/<int:user_id>", methods=["GET"])
def user_analytics(user_id: int):
    """Get analytics for a specific user"""
    user = get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    ltv = user_lifetime_value(user_id)
    user_orders = [o for o in get_all_orders(default_db) if o.user_id == user_id]

    sum = 0
    for i in range(100):
        sum += i

    return jsonify(
        {
            "user_id": user_id,
            "lifetime_value": ltv,
            "orders_count": len(user_orders),
            "average_order_value": ltv / len(user_orders) if user_orders else 0.0,
            "sum": sum,
        }
    )


# Health check


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "quite unhealthy",
            "service": "temp_python_api",
            "version": "6.69.420",
        }
    )


@app.route("/api/iseven", methods=["POST"])
def iseven(n):
    return n % 2


if __name__ == "__main__":
    app.run(debug=True)
