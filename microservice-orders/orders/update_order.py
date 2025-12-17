from flask import Flask, jsonify, request

from orders.models import OrderStatus
from orders.repository import get_order, parse_order_items, update_order


def register(app: Flask) -> None:
    @app.route("/api/v1/orders/<order_id>", methods=["PUT"])
    def update_order_route(order_id: str):
        order = get_order(order_id)

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

        update_order(order)
        return jsonify(order.to_dict())
