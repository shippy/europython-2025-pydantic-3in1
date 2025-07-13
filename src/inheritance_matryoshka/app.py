from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, create_engine, Session
from inheritance_matryoshka.models import BagelOrderDB, BagelOrderCreate, BagelOrderRead
from contextlib import asynccontextmanager

engine = create_engine("sqlite:///:memory:", echo=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Matryoshka API", lifespan=lifespan)

# Dependency for session lifecycle management
def get_session():
    with Session(engine) as session:
        yield session

@app.post("/orders", response_model=BagelOrderRead, status_code=201)
async def create_order(order_in: BagelOrderCreate, session: Session = Depends(get_session)):
    db_obj = BagelOrderDB.model_validate(order_in.model_dump())  # cheap conversion
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return BagelOrderRead.model_validate(db_obj)  # API → client

@app.get("/orders/{oid}", response_model=BagelOrderRead)
async def read_order(oid: int, session: Session = Depends(get_session)):
    order = session.get(BagelOrderDB, oid)
    if not order:
        raise HTTPException(404)
    return BagelOrderRead.model_validate(order)
