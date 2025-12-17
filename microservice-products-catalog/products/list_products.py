from flask import Flask, jsonify, request

from products.repository import get_all_products


def register(app: Flask) -> None:
    @app.route("/api/v1/products", methods=["GET"])
    def list_products():
        category_filter = request.args.get("category")
        products = get_all_products(category_filter)
        return jsonify({"products": [p.to_dict() for p in products], "count": len(products)})
