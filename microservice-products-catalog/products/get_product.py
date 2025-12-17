from flask import Flask, jsonify

from products.repository import get_product


def register(app: Flask) -> None:
    @app.route("/api/v1/products/<int:product_id>", methods=["GET"])
    def get_product_by_id(product_id: int):
        product = get_product(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product.to_dict())
