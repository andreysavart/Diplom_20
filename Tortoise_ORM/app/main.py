from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise
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
    await init_db()
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
    pass


app = FastAPI(title='Detail_Ordering', lifespan=lifespan)


app.include_router(bolt.router)
app.include_router(bolt_joint.router)
app.include_router(nut.router)
app.include_router(order.router)
app.include_router(washer.router)

if __name__=="__main__":
    uvicorn.run('app.main:app', reload=True)
