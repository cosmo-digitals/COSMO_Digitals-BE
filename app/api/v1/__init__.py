from fastapi import APIRouter
# from .endpoints import contact, users, auth
from .endpoints import contact, users, auth  # remove auth if unused

router = APIRouter()
router.include_router(contact.router)
router.include_router(users.router)
# router.include_router(auth.router)
