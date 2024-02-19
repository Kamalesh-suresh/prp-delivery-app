import motor.motor_asyncio
from beanie import init_beanie

from config import MONGODB_CONNECTION_STRING
from models import User
from schema_model.menus import Menu
from schema_model.restaurants import Restaurant


async def init_db():
    connection_string = MONGODB_CONNECTION_STRING
    if not connection_string:
        raise ValueError("MONGODB_CONNECTION_STRING environment variable is not set")

    client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
    await init_beanie(
        database=client["foody"], document_models=[User, Restaurant, Menu]
    )
