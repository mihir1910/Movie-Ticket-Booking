import os
from motor.motor_asyncio import AsyncIOMotorClient

client = None


async def connect_db():
    global client
    try:
        client = AsyncIOMotorClient(os.environ["MONGO_URL"])
        await client.admin.command("ping")
        print("DB Connected")
    except Exception as error:
        print("DB Connection Failed ", error)
