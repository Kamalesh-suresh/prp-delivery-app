from config import MONGODB_CONNECTION_STRING
import motor.motor_asyncio
from models import User
from beanie import init_beanie

async def init_db():
    connection_string = MONGODB_CONNECTION_STRING
    if not connection_string:
        raise ValueError("MONGODB_CONNECTION_STRING environment variable is not set")

    client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
    await init_beanie(database=client["foody"], document_models=[User])