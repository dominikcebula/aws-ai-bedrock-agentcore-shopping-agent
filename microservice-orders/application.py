from flask import Flask, jsonify

application = Flask(__name__)

@application.route("/")
def health_check():
    return jsonify({"status": "healthy", "service": "orders"})


@application.route("/api/v1/orders", methods=["GET"])
def list_orders():
    return jsonify({"orders": [], "count": 0})


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
