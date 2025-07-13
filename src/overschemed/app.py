"""
Run: uv run uvicorn overschemed.app:app --reload
"""
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine, Session
from overschemed.domain import Order
from overschemed.schemas import OrderIn, OrderOut, OrderDB, to_domain, from_domain

engine = create_engine("sqlite:///:memory:", echo=False)
SQLModel.metadata.create_all(engine)

app = FastAPI(title="Bounded-Contexts API")

@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order_in: OrderIn):
    domain_obj = to_domain(order_in)
    db_obj = OrderDB(**domain_obj.__dict__)
    with Session(engine) as s:
        s.add(db_obj)
        s.commit()
        s.refresh(db_obj)
        return from_domain(to_domain(db_obj), OrderOut)

@app.get("/orders/{oid}", response_model=OrderOut)
def read_order(oid: int):
    with Session(engine) as s:
        row = s.get(OrderDB, oid)
        if not row:
            raise HTTPException(404)
        return from_domain(to_domain(row), OrderOut)
