from flask import Flask

from orders.cancel_order import register as register_cancel_order
from orders.create_order import register as register_create_order
from orders.get_order import register as register_get_order
from orders.health_check import register as register_health_check
from orders.list_orders import register as register_list_orders
from orders.update_order import register as register_update_order


def create_app() -> Flask:
    app = Flask(__name__)
    register_health_check(app)
    register_create_order(app)
    register_list_orders(app)
    register_get_order(app)
    register_update_order(app)
    register_cancel_order(app)
    return app
