from flask import Flask

from products.get_product import register as register_get_product
from products.health_check import register as register_health_check
from products.list_products import register as register_list_products


def create_app() -> Flask:
    app = Flask(__name__)
    register_health_check(app)
    register_list_products(app)
    register_get_product(app)
    return app
