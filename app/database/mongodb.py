# app/database/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
import os

_MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
_DB_NAME = os.getenv("MONGO_DB_NAME", "contact_db")

client: AsyncIOMotorClient | None = None


async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(_MONGO_URI)


async def close_mongo_connection():
    if client:
        client.close()


def get_db():
    if client is None:
        raise RuntimeError("Mongo client not initialised")
    return client[_DB_NAME]
