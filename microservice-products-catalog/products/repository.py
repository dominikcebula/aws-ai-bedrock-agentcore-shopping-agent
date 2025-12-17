from products.models import Product

# In-memory product catalog
_products: list[Product] = [
    Product(id=1, name="Wireless Gaming Mouse", price=59.99, category="Mice", stock=150),
    Product(id=2, name="Mechanical Gaming Keyboard", price=129.99, category="Keyboards", stock=80),
    Product(id=3, name="27-inch 4K Monitor", price=349.99, category="Monitors", stock=45),
    Product(id=4, name="Noise-Cancelling Headset", price=89.99, category="Headsets", stock=120),
    Product(id=5, name="Ergonomic Vertical Mouse", price=39.99, category="Mice", stock=95),
    Product(id=6, name="Compact Wireless Keyboard", price=49.99, category="Keyboards", stock=110),
    Product(id=7, name="34-inch Ultrawide Monitor", price=599.99, category="Monitors", stock=30),
    Product(id=8, name="USB-C Docking Station", price=149.99, category="Accessories", stock=75),
    Product(id=9, name="RGB Gaming Headset", price=69.99, category="Headsets", stock=100),
    Product(id=10, name="Trackball Mouse", price=44.99, category="Mice", stock=60),
    Product(id=11, name="Mechanical Numpad", price=34.99, category="Keyboards", stock=85),
    Product(id=12, name="Portable USB Monitor", price=199.99, category="Monitors", stock=55),
    Product(id=13, name="Webcam 1080p HD", price=79.99, category="Cameras", stock=140),
    Product(id=14, name="USB Microphone", price=99.99, category="Audio", stock=90),
    Product(id=15, name="Large Gaming Mouse Pad", price=24.99, category="Accessories", stock=200),
    Product(id=16, name="Monitor Stand with USB Hub", price=59.99, category="Accessories", stock=70),
    Product(id=17, name="Wireless Earbuds", price=79.99, category="Headsets", stock=130),
    Product(id=18, name="Bluetooth Keyboard and Mouse Combo", price=69.99, category="Keyboards", stock=65),
    Product(id=19, name="4K Webcam with Ring Light", price=129.99, category="Cameras", stock=50),
    Product(id=20, name="USB Hub 7-Port", price=29.99, category="Accessories", stock=180),
    Product(id=21, name="Dell XPS 15 Laptop", price=1499.99, category="Laptops", stock=25),
    Product(id=22, name="HP Spectre x360", price=1299.99, category="Laptops", stock=30),
    Product(id=23, name="ASUS ROG Zephyrus G14", price=1599.99, category="Laptops", stock=20),
    Product(id=24, name="Lenovo ThinkPad X1 Carbon", price=1449.99, category="Laptops", stock=35),
    Product(id=25, name="Apple MacBook Air M3", price=1099.99, category="Laptops", stock=40),
    Product(id=26, name="Dell Inspiron 14", price=699.99, category="Laptops", stock=50),
    Product(id=27, name="HP Pavilion 15", price=649.99, category="Laptops", stock=45),
    Product(id=28, name="ASUS ZenBook 14", price=899.99, category="Laptops", stock=35),
    Product(id=29, name="Lenovo ThinkPad T14", price=1199.99, category="Laptops", stock=28),
    Product(id=30, name="Apple MacBook Pro 14 M3", price=1999.99, category="Laptops", stock=22),
]


def get_all_products(category_filter: str | None = None) -> list[Product]:
    if category_filter:
        return [p for p in _products if p.category.lower() == category_filter.lower()]
    return _products


def get_product(product_id: int) -> Product | None:
    for product in _products:
        if product.id == product_id:
            return product
    return None
