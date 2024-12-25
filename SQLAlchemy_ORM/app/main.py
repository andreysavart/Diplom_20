from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from app.backend.db import init_db
from app.routers import (
    bolt,
    bolt_joint,
    nut,
    order,
    washer,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    pass


app = FastAPI(title='Detail_Ordering', lifespan=lifespan)


@app.get("/")
async def welcome():
    return {"message": "Welcome to Detail_Ordering"}

app.include_router(bolt.router)
app.include_router(bolt_joint.router)
app.include_router(nut.router)
app.include_router(order.router)
app.include_router(washer.router)

if __name__=="__main__":
    uvicorn.run('app.main:app', reload=True)
