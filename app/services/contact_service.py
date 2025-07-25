from datetime import datetime
from app.database.mongodb import get_db
from app.schemas.contact import ContactCreate

async def save_contact(data: ContactCreate) -> str:
    """
    Persist a contact in MongoDB and return the inserted id as a string.
    """
    db = get_db()
    payload = data.dict()
    payload["created_at"] = datetime.utcnow()  # ✅ Add timestamp
    result = await db["contacts"].insert_one(payload)
    return str(result.inserted_id)
