import uuid
from datetime import datetime

from orders.models import Order, OrderItem, OrderStatus

# In-memory storage
_orders_db: dict[str, Order] = {}


def parse_order_items(items_data: list[dict]) -> list[OrderItem]:
    items = []
    for item in items_data:
        items.append(
            OrderItem(
                product_id=item["product_id"],
                name=item["name"],
                price=float(item["price"]),
                quantity=int(item["quantity"]),
            )
        )
    return items


def create_order(items: list[OrderItem]) -> Order:
    now = datetime.utcnow()
    order = Order(
        id=str(uuid.uuid4()),
        items=items,
        status=OrderStatus.CONFIRMED,
        created_at=now,
        updated_at=now,
    )
    _orders_db[order.id] = order
    return order


def get_order(order_id: str) -> Order | None:
    return _orders_db.get(order_id)


def get_all_orders(status_filter: OrderStatus | None = None) -> list[Order]:
    orders = list(_orders_db.values())
    if status_filter:
        orders = [o for o in orders if o.status == status_filter]
    return orders


def update_order(order: Order) -> Order:
    order.updated_at = datetime.utcnow()
    _orders_db[order.id] = order
    return order


def clear_orders() -> None:
    _orders_db.clear()
