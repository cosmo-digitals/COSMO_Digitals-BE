# app/database/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
import os

_MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
_DB_NAME = os.getenv("MONGO_DB_NAME", "contact_db")

client: AsyncIOMotorClient | None = None


async def connect_to_mongo():
    global client
    print(f"Connecting to MongoDB at {_MONGO_URI}...")
    print(f"Using database: {_DB_NAME}")
    if client is not None:
        print("MongoDB client already initialized.")
        return
    try:
        client = AsyncIOMotorClient(_MONGO_URI)
        # Test the connection
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    if client:
        client.close()


def get_db():
    if client is None:
        raise RuntimeError("Mongo client not initialised")
    
    # If the URI already contains the database name, use it directly
    if "/" in _MONGO_URI.split("mongodb")[1]:
        # Extract database name from URI
        db_name = _MONGO_URI.split("/")[-1].split("?")[0]
        return client[db_name]
    else:
        return client[_DB_NAME]
