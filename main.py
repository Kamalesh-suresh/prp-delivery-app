"""This module contains the main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from mangum import Mangum

from database import init_db
from routes.restaurants import restaurants_router
# from users import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async context manager to initialize the database."""
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


handler = Mangum(app)


# app.include_router(users_router, prefix="/users")
app.include_router(restaurants_router, prefix="/restaurants")
