from datetime import datetime, UTC
from sqlalchemy import JSON, Column, DateTime
from sqlmodel import SQLModel, Field

class BagelOrder(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_name: str
    bagel_type: str
    toppings: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    quantity: int = 1
    status: str = "pending"  # will round‐trip to clients & LLMs
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        sa_column=Column(DateTime(timezone=True))
    )
