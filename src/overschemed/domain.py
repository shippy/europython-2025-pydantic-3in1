from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class Order:
    id: int | None
    customer_name: str
    bagel_type: str
    toppings: list[str]
    quantity: int
    status: str
    created_at: datetime
