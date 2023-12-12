import motor
import motor.motor_asyncio
from models import User
from beanie import init_beanie


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://kamalesh:kamal1234@cluster0.y53uz6w.mongodb.net/?retryWrites=true&w=majority")
    print(client,"ssssssssssssssssssssssssss")
    await init_beanie(database=client["foody"], document_models=[User])