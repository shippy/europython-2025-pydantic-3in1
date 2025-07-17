from datetime import datetime
from sqlalchemy import JSON, Column
from sqlmodel import SQLModel, Field
from pydantic.json_schema import SkipJsonSchema

class BagelOrder(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_name: str
    bagel_type: str
    toppings: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    quantity: int = 1
    status: str = "pending"  # will round‐trip to clients & LLMs
    created_at: datetime = Field(
        default_factory=datetime.now,
    )
    admin_notes: SkipJsonSchema[str | None]
