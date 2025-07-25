"""
Run: uv run uvicorn everything_bagel.app:app --reload
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, create_engine, Session
from everything_bagel.model import BagelOrder
from contextlib import asynccontextmanager
from typing import Annotated, Generator

engine = create_engine("sqlite:///take0.db", echo=False, connect_args={"check_same_thread": False})

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Everything-Bagel API", lifespan=lifespan)

# Dependency for session lifecycle management
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/orders", response_model=BagelOrder, status_code=201)
async def create_order(order: BagelOrder, session: SessionDep):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

@app.get("/orders/{order_id}", response_model=BagelOrder)
async def read_order(order_id: int, session: SessionDep):
    order = session.get(BagelOrder, order_id)
    if not order:
        raise HTTPException(404)
    return order
