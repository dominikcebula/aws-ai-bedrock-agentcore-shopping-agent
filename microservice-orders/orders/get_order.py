from flask import Flask, jsonify

from orders.repository import get_order


def register(app: Flask) -> None:
    @app.route("/api/v1/orders/<order_id>", methods=["GET"])
    def get_order_route(order_id: str):
        order = get_order(order_id)

        if not order:
            return jsonify({"error": "Order not found"}), 404

        return jsonify(order.to_dict())
