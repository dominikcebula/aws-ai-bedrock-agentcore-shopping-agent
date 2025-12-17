from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    price: float
    category: str
    stock: int

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "stock": self.stock,
        }
