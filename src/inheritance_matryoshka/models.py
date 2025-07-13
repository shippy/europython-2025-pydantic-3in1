from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import JSON, Column
from sqlmodel import SQLModel, Field as SQLModelField

# -------- shared core --------
class BagelType(str, Enum):
    plain = "plain"
    sesame = "sesame"
    everything = "everything"
    poppy = "poppy"

class ToppingType(str, Enum):
    cream_cheese = "cream-cheese"
    lox = "lox"
    butter = "butter"
    none = "none"

class BagelOrderBase(BaseModel):
    customer_name: str
    bagel_type: BagelType
    toppings: list[str] = Field(default_factory=list)
    quantity: int = 1

# -------- DB / ORM --------
class BagelOrderDB(BagelOrderBase, SQLModel, table=True):
    id: int | None = SQLModelField(default=None, primary_key=True)
    status: str = "pending"
    created_at: datetime = SQLModelField(default_factory=datetime.utcnow)
    toppings: list[str] = SQLModelField(default_factory=list, sa_column=Column(JSON))

# -------- API layer --------
class BagelOrderCreate(BagelOrderBase):
    model_config = ConfigDict(extra="forbid")

class BagelOrderRead(BagelOrderDB):
    """What we return to clients (includes DB fields)."""
    # FIXME: Actually need to fix inheritance here

# -------- LLM layer --------
class BagelOrderLLM(BagelOrderBase):
    """Stricter toppings list for the model."""
    toppings: list[ToppingType] = []
