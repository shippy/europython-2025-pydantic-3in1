from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, create_engine, Session
from inheritance_matryoshka.models import BagelOrderDB, BagelOrderCreate, BagelOrderRead
from contextlib import asynccontextmanager
from typing import Annotated, Generator

engine = create_engine("sqlite:///take1.db", echo=False, connect_args={"check_same_thread": False})

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Matryoshka API", lifespan=lifespan)

# Dependency for session lifecycle management
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/orders", response_model=BagelOrderRead, status_code=201)
async def create_order(order_in: BagelOrderCreate, session: SessionDep):
    db_obj = BagelOrderDB.model_validate(order_in.model_dump())  # cheap conversion
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return BagelOrderRead.model_validate(db_obj.model_dump())  # API → client

@app.get("/orders/{oid}", response_model=BagelOrderRead)
async def read_order(oid: int, session: SessionDep):
    order = session.get(BagelOrderDB, oid)
    if not order:
        raise HTTPException(404)
    return BagelOrderRead.model_validate(order.model_dump())
