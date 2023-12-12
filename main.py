from typing import Union

from fastapi import FastAPI

from dishes import users_router
from database import init_db
from mangum import Mangum
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


handler = Mangum(app)


app.include_router(users_router, prefix='/users')
