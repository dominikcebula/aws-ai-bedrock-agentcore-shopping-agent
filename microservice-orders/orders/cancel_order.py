from flask import Flask, jsonify

from orders.models import OrderStatus
from orders.repository import get_order, update_order


def register(app: Flask) -> None:
    @app.route("/api/v1/orders/<order_id>", methods=["DELETE"])
    def cancel_order(order_id: str):
        order = get_order(order_id)

        if not order:
            return jsonify({"error": "Order not found"}), 404

        if order.status == OrderStatus.CANCELLED:
            return jsonify({"error": "Order is already cancelled"}), 400

        order.status = OrderStatus.CANCELLED
        update_order(order)
        return jsonify(order.to_dict())
