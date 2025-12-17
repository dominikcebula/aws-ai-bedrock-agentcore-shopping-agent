from flask import Flask, jsonify


def register(app: Flask) -> None:
    @app.route("/")
    def health_check():
        return jsonify({"status": "healthy", "service": "orders"})
