from fastapi import APIRouter
from .endpoints import contact, users, items, auth   # keep existing ones!

router = APIRouter()
router.include_router(contact.router)
router.include_router(users.router)
router.include_router(items.router)
router.include_router(auth.router)
