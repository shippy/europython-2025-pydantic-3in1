"""
Run:  uvicorn take_0:app --reload
"""
from decimal import Decimal
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.json_schema import SkipJsonSchema

app = FastAPI()


class BagelOrder(BaseModel):
    # ---------- Public (API/LLM) ----------
    order_id: int | None = None
    toppings: List[str]
    coupon: str | None = None
    total_usd: Decimal

    # ---------- Internal / DB-only ----------
    admin_notes: SkipJsonSchema[str | None] = None
    topping_ids: SkipJsonSchema[List[int]] = []

# Hand the same schema to the LLM “function call” interface
LLM_TOOL_SCHEMA = {
    "name": "create_bagel_order",
    "description": "Create a new bagel order",
    "parameters": BagelOrder.model_json_schema()
}


@app.post("/orders", response_model=BagelOrder)
def create_order(order: BagelOrder):
    return order  # For simplicity