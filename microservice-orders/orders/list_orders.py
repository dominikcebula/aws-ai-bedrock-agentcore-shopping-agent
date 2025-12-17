from flask import Flask, jsonify, request

from orders.models import OrderStatus
from orders.repository import get_all_orders


def register(app: Flask) -> None:
    @app.route("/api/v1/orders", methods=["GET"])
    def list_orders():
        status_filter = request.args.get("status")

        if status_filter:
            try:
                status = OrderStatus(status_filter)
                orders = get_all_orders(status)
            except ValueError:
                return jsonify({"error": f"Invalid status: {status_filter}"}), 400
        else:
            orders = get_all_orders()

        return jsonify({"orders": [order.to_dict() for order in orders], "count": len(orders)})
