import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from flask import Flask, jsonify, request

application = Flask(__name__)


class OrderStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    product_id: str
    name: str
    price: float
    quantity: int

    @property
    def total(self) -> float:
        return self.price * self.quantity

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "total": self.total
        }


@dataclass
class Order:
    id: str
    items: list[OrderItem]
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    @property
    def total_value(self) -> float:
        return sum(item.total for item in self.items)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "items": [item.to_dict() for item in self.items],
            "total_value": self.total_value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


# In-memory storage
orders_db: dict[str, Order] = {}


def parse_order_items(items_data: list[dict]) -> list[OrderItem]:
    items = []
    for item in items_data:
        items.append(OrderItem(
            product_id=item["product_id"],
            name=item["name"],
            price=float(item["price"]),
            quantity=int(item["quantity"])
        ))
    return items


@application.route("/")
def health_check():
    return jsonify({"status": "healthy", "service": "orders"})


@application.route("/api/v1/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data or "items" not in data or not data["items"]:
        return jsonify({"error": "Order must contain at least one item"}), 400

    try:
        items = parse_order_items(data["items"])
    except (KeyError, ValueError) as e:
        return jsonify({"error": f"Invalid item data: {str(e)}"}), 400

    now = datetime.utcnow()
    order = Order(
        id=str(uuid.uuid4()),
        items=items,
        status=OrderStatus.CONFIRMED,
        created_at=now,
        updated_at=now
    )

    orders_db[order.id] = order
    return jsonify(order.to_dict()), 201


@application.route("/api/v1/orders", methods=["GET"])
def list_orders():
    status_filter = request.args.get("status")

    orders = list(orders_db.values())

    if status_filter:
        try:
            status = OrderStatus(status_filter)
            orders = [o for o in orders if o.status == status]
        except ValueError:
            return jsonify({"error": f"Invalid status: {status_filter}"}), 400

    return jsonify({
        "orders": [order.to_dict() for order in orders],
        "count": len(orders)
    })


@application.route("/api/v1/orders/<order_id>", methods=["GET"])
def get_order(order_id: str):
    order = orders_db.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(order.to_dict())


@application.route("/api/v1/orders/<order_id>", methods=["PUT"])
def update_order(order_id: str):
    order = orders_db.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    if order.status == OrderStatus.CANCELLED:
        return jsonify({"error": "Cannot update a cancelled order"}), 400

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "items" in data:
        if not data["items"]:
            return jsonify({"error": "Order must contain at least one item"}), 400
        try:
            order.items = parse_order_items(data["items"])
        except (KeyError, ValueError) as e:
            return jsonify({"error": f"Invalid item data: {str(e)}"}), 400

    if "status" in data:
        try:
            new_status = OrderStatus(data["status"])
            if order.status == OrderStatus.CANCELLED:
                return jsonify({"error": "Cannot change status of cancelled order"}), 400
            order.status = new_status
        except ValueError:
            return jsonify({"error": f"Invalid status: {data['status']}"}), 400

    order.updated_at = datetime.utcnow()

    return jsonify(order.to_dict())


@application.route("/api/v1/orders/<order_id>", methods=["DELETE"])
def cancel_order(order_id: str):
    order = orders_db.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    if order.status == OrderStatus.CANCELLED:
        return jsonify({"error": "Order is already cancelled"}), 400

    if order.status in [OrderStatus.CONFIRMED]:
        return jsonify({"error": "Cannot cancel an order that has been shipped or delivered"}), 400

    order.status = OrderStatus.CANCELLED
    order.updated_at = datetime.utcnow()

    return jsonify(order.to_dict())


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
