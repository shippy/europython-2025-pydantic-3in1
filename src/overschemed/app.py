"""
Run: uv run uvicorn overschemed.app:app --reload
"""
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine, Session
from overschemed.domain import Order  # noqa: F401
from overschemed.schemas import OrderIn, OrderOut, OrderDB, to_domain, from_domain
from typing import Annotated, Generator
from fastapi import Depends
from contextlib import asynccontextmanager

engine = create_engine("sqlite:///:memory:", echo=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Bounded-Contexts API", lifespan=lifespan)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order_in: OrderIn, session: SessionDep):
    domain_obj = to_domain(order_in)
    db_obj = OrderDB(**domain_obj.__dict__)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    domain_obj = to_domain(db_obj)
    return from_domain(domain_obj, OrderOut)

@app.get("/orders/{oid}", response_model=OrderOut)
def read_order(oid: int, session: SessionDep):
    row = session.get(OrderDB, oid)
    if not row:
        raise HTTPException(404)
    domain_obj = to_domain(row)
    return from_domain(domain_obj, OrderOut)
