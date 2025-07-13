# bagel/domain.py
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlmodel import SQLModel, Field


@dataclass(slots=True)
class Order:                     # ← business entity, NO validation
    id: int | None
    customer_name: str
    bagel_type: str
    toppings: list[str]
    quantity: int
    status: str
    created_at: datetime

# ---------------------- SCHEMAS ----------------------
class OrderIn(BaseModel):                       # API input
    customer_name: str
    bagel_type: str
    toppings: list[str] = []
    quantity: int = 1
    model_config = ConfigDict(extra="forbid")

class OrderOut(BaseModel):                      # API output
    id: int
    status: str
    created_at: datetime

class OrderDB(SQLModel, table=True):            # Storage
    id: int | None = Field(primary_key=True)
    customer_name: str
    bagel_type: str
    toppings: list[str]
    quantity: int
    status: str
    created_at: datetime

class OrderLLM(BaseModel):                      # LLM
    customer_name: str
    bagel_type: str
    quantity: int

# --------------- MAPPERS ---------------
def to_domain(obj) -> Order:
    if isinstance(obj, (OrderIn, OrderOut, OrderDB, OrderLLM)):
        return Order(**obj.model_dump(), id=getattr(obj, "id", None),
                     status=getattr(obj, "status", "pending"),
                     created_at=getattr(obj, "created_at", datetime.utcnow()))
    raise TypeError("unsupported type")

def from_domain(domain: Order, target):
    if target is OrderDB:
        return OrderDB(**domain.__dict__)
    if target is OrderOut:
        return OrderOut(id=domain.id, status=domain.status, created_at=domain.created_at)
    # … etc …
