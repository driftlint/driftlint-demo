from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Order:
    id: int
    customer: str
    total_cents: int
    created_at: datetime = field(default_factory=datetime.utcnow)


class OrderStore:
    def __init__(self):
        self._orders: List[Order] = []
        self._next_id = 1

    def list_orders(self):
        return list(self._orders)

    def create_order(self, customer: str, total_cents: int):
        order = Order(id=self._next_id, customer=customer, total_cents=total_cents)
        self._orders.append(order)
        self._next_id += 1
        return order
