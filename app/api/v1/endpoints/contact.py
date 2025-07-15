"""
This module defines the API endpoint for creating contact entries.
It handles HTTP POST requests and interacts with the contact service
to save contact data into the database.
"""

from fastapi import APIRouter, status
from app.schemas.contact import ContactCreate
from app.services.contact_service import save_contact

router = APIRouter(tags=["contact"])


@router.post("/contact/create", status_code=status.HTTP_201_CREATED)
async def create_contact(data: ContactCreate):
    """
    Create a new contact entry using the provided data.
    Args: data (ContactCreate): The contact data from the client.
    Returns: dict: A dictionary containing the inserted contact ID and a
    """
    inserted_id = await save_contact(data)
    return {"id": inserted_id, "message": "Contact saved"}
