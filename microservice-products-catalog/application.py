from flask import Flask, jsonify

application = Flask(__name__)

# Sample products catalog with 30 items (computer accessories and laptops)
PRODUCTS = [
    {"id": 1, "name": "Wireless Gaming Mouse", "price": 59.99, "category": "Mice", "stock": 150},
    {"id": 2, "name": "Mechanical Gaming Keyboard", "price": 129.99, "category": "Keyboards", "stock": 80},
    {"id": 3, "name": "27-inch 4K Monitor", "price": 349.99, "category": "Monitors", "stock": 45},
    {"id": 4, "name": "Noise-Cancelling Headset", "price": 89.99, "category": "Headsets", "stock": 120},
    {"id": 5, "name": "Ergonomic Vertical Mouse", "price": 39.99, "category": "Mice", "stock": 95},
    {"id": 6, "name": "Compact Wireless Keyboard", "price": 49.99, "category": "Keyboards", "stock": 110},
    {"id": 7, "name": "34-inch Ultrawide Monitor", "price": 599.99, "category": "Monitors", "stock": 30},
    {"id": 8, "name": "USB-C Docking Station", "price": 149.99, "category": "Accessories", "stock": 75},
    {"id": 9, "name": "RGB Gaming Headset", "price": 69.99, "category": "Headsets", "stock": 100},
    {"id": 10, "name": "Trackball Mouse", "price": 44.99, "category": "Mice", "stock": 60},
    {"id": 11, "name": "Mechanical Numpad", "price": 34.99, "category": "Keyboards", "stock": 85},
    {"id": 12, "name": "Portable USB Monitor", "price": 199.99, "category": "Monitors", "stock": 55},
    {"id": 13, "name": "Webcam 1080p HD", "price": 79.99, "category": "Cameras", "stock": 140},
    {"id": 14, "name": "USB Microphone", "price": 99.99, "category": "Audio", "stock": 90},
    {"id": 15, "name": "Large Gaming Mouse Pad", "price": 24.99, "category": "Accessories", "stock": 200},
    {"id": 16, "name": "Monitor Stand with USB Hub", "price": 59.99, "category": "Accessories", "stock": 70},
    {"id": 17, "name": "Wireless Earbuds", "price": 79.99, "category": "Headsets", "stock": 130},
    {"id": 18, "name": "Bluetooth Keyboard and Mouse Combo", "price": 69.99, "category": "Keyboards", "stock": 65},
    {"id": 19, "name": "4K Webcam with Ring Light", "price": 129.99, "category": "Cameras", "stock": 50},
    {"id": 20, "name": "USB Hub 7-Port", "price": 29.99, "category": "Accessories", "stock": 180},
    {"id": 21, "name": "Dell XPS 15 Laptop", "price": 1499.99, "category": "Laptops", "stock": 25},
    {"id": 22, "name": "HP Spectre x360", "price": 1299.99, "category": "Laptops", "stock": 30},
    {"id": 23, "name": "ASUS ROG Zephyrus G14", "price": 1599.99, "category": "Laptops", "stock": 20},
    {"id": 24, "name": "Lenovo ThinkPad X1 Carbon", "price": 1449.99, "category": "Laptops", "stock": 35},
    {"id": 25, "name": "Apple MacBook Air M3", "price": 1099.99, "category": "Laptops", "stock": 40},
    {"id": 26, "name": "Dell Inspiron 14", "price": 699.99, "category": "Laptops", "stock": 50},
    {"id": 27, "name": "HP Pavilion 15", "price": 649.99, "category": "Laptops", "stock": 45},
    {"id": 28, "name": "ASUS ZenBook 14", "price": 899.99, "category": "Laptops", "stock": 35},
    {"id": 29, "name": "Lenovo ThinkPad T14", "price": 1199.99, "category": "Laptops", "stock": 28},
    {"id": 30, "name": "Apple MacBook Pro 14 M3", "price": 1999.99, "category": "Laptops", "stock": 22},
]


@application.route("/")
def health_check():
    return jsonify({"status": "healthy", "service": "products-catalog"})


@application.route("/api/v1/products", methods=["GET"])
def list_products():
    return jsonify({"products": PRODUCTS, "count": len(PRODUCTS)})


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
