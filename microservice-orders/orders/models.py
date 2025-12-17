from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    product_id: str
    name: str
    price: float
    quantity: int

    @property
    def total(self) -> float:
        return self.price * self.quantity

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "total": self.total,
        }


@dataclass
class Order:
    id: str
    items: list[OrderItem]
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    @property
    def total_value(self) -> float:
        return sum(item.total for item in self.items)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "items": [item.to_dict() for item in self.items],
            "total_value": self.total_value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
