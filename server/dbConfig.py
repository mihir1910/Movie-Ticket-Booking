import os
from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None


async def connect_db():
    global client, db
    try:
        client = AsyncIOMotorClient(os.environ["MONGO_URL"])
        db = client.get_default_database()
        await client.admin.command("ping")
        print("DB Connected")
    except Exception as error:
        print("DB Connection Failed ", error)
