from flask import Flask, jsonify, request

from orders.repository import create_order, parse_order_items


def register(app: Flask) -> None:
    @app.route("/api/v1/orders", methods=["POST"])
    def create_order_route():
        data = request.get_json()

        if not data or "items" not in data or not data["items"]:
            return jsonify({"error": "Order must contain at least one item"}), 400

        try:
            items = parse_order_items(data["items"])
        except (KeyError, ValueError) as e:
            return jsonify({"error": f"Invalid item data: {str(e)}"}), 400

        order = create_order(items)
        return jsonify(order.to_dict()), 201
