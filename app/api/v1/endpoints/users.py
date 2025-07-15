from fastapi import APIRouter, Depends
from app.database.mongodb import get_db

router = APIRouter()


@router.get("/")
async def get_users(db=Depends(get_db)):
    users = await db["users"].find().to_list(100)
    return users
