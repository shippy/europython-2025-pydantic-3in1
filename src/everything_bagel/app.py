"""
Run: uv run uvicorn everything_bagel.app:app --reload
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, create_engine, Session
from everything_bagel.model import BagelOrder
from contextlib import asynccontextmanager

engine = create_engine("sqlite:///:memory:", echo=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Everything-Bagel API", lifespan=lifespan)

# Dependency for session lifecycle management
def get_session():
    with Session(engine) as session:
        yield session

@app.post("/orders", response_model=BagelOrder, status_code=201)
async def create_order(order: BagelOrder, session: Session = Depends(get_session)):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

@app.get("/orders/{order_id}", response_model=BagelOrder)
async def read_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(BagelOrder, order_id)
    if not order:
        raise HTTPException(404)
    return order
