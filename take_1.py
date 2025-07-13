"""
Run: uvicorn take_1:app --reload
"""

# bagel/models.py
from datetime import datetime
from typing import Literal
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, ConfigDict

class BagelOrderBase(BaseModel):
    customer_name: str
    bagel_type: str
    toppings: list[str] = []
    quantity: int = 1

# ----- DB layer -----
class BagelOrderDB(BagelOrderBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ----- FastAPI -----
class BagelOrderCreate(BagelOrderBase):
    model_config = ConfigDict(extra="forbid")    # user can’t set status/created_at

class BagelOrderRead(BagelOrderDB):
    pass                                         # expose the whole record

# ----- LLM -----
class BagelOrderLLM(BagelOrderBase):
    toppings: list[Literal["sesame","everything","poppy","plain"]] = []
