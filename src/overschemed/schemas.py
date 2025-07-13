from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import JSON, Column
from sqlmodel import SQLModel, Field as SQLModelField
from overschemed.domain import Order

# ----- API -----
class OrderIn(BaseModel):
    customer_name: str
    bagel_type: str
    toppings: list[str] = []
    quantity: int = 1
    model_config = ConfigDict(extra="forbid")

class OrderOut(BaseModel):
    id: int
    status: str
    created_at: datetime

# ----- DB -----
class OrderDB(SQLModel, table=True):
    id: int | None = SQLModelField(primary_key=True)
    customer_name: str
    bagel_type: str
    toppings: list[str] = SQLModelField(default_factory=list, sa_column=Column(JSON))
    quantity: int
    status: str
    created_at: datetime

# ----- LLM -----
class OrderLLM(BaseModel):
    customer_name: str
    bagel_type: str
    quantity: int

# ---------- mappers ----------
def to_domain(source) -> Order:
    if isinstance(source, Order):
        return source
    data = source.model_dump()
    return Order(
        id=data.get("id"),
        customer_name=data["customer_name"],
        bagel_type=data["bagel_type"],
        toppings=data.get("toppings", []),
        quantity=data.get("quantity", 1),
        status=data.get("status", "pending"),
        created_at=data.get("created_at") or datetime.utcnow(),
    )

def from_domain(domain: Order, target):
    if target is OrderDB:
        return OrderDB(**domain.__dict__)
    if target is OrderOut:
        return OrderOut(id=domain.id, status=domain.status, created_at=domain.created_at)
    if target is OrderLLM:
        return OrderLLM(
            customer_name=domain.customer_name,
            bagel_type=domain.bagel_type,
            quantity=domain.quantity,
        )
    raise TypeError(f"unknown target {target}")
