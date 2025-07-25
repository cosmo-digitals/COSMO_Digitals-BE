from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
async def login_check():
    return {"message": "Auth route works!"}