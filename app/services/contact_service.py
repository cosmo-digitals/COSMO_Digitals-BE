from app.database.mongodb import get_db
from app.schemas.contact import ContactCreate
from app.utils.email_utils import send_contact_email

async def save_contact(contact: ContactCreate) -> str:
    db = get_db()
    result = await db.contacts.insert_one(contact.model_dump())
    await send_contact_email(contact)        # fire‑and‑forget
    return str(result.inserted_id)
