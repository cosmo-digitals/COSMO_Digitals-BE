from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.schemas.contact import ContactCreate, ContactInDB
from app.services.contact_service import save_contact
from app.dependencies.email_provider import email_sender  # ✅ Use this
from app.database.mongodb import get_db

router = APIRouter(prefix="/api/v1", tags=["contact"])


@router.post("/contact", status_code=status.HTTP_201_CREATED)
async def create_contact(data: ContactCreate):
    """
    • Save to MongoDB
    • Send notification email
    """
    inserted_id = await save_contact(data)
    try:
        await email_sender.send_contact_email(data.dict())  # ✅ Fixed usage
        return {"id": inserted_id, "message": "Contact saved & mail sent"}
    except Exception as exc:
        # Log the error but don't fail the request since data is saved
        print(f"Email sending failed: {exc}")
        return {"id": inserted_id, "message": "Contact saved (email notification failed)"}


@router.get("/contact", response_model=list[ContactInDB])
async def list_contacts(db=Depends(get_db)):
    """
    Return all contacts (newest first) for the admin dashboard.
    """
    docs = await db["contacts"].find().sort("_id", -1).to_list(1000)
    normalized_docs = []
    
    for doc in docs:
        # Normalize the document keys
        normalized_doc = {
            "id": str(doc.pop("_id")),
            "first_name": doc.get("first_name", ""),
            "last_name": doc.get("last_name", ""),
            "email": doc.get("email", ""),
            "phone_number": doc.get("phone_number", ""),
            "message": doc.get("message", ""),
            "services": doc.get("services", []),
            "created_at": doc.get("created_at")
        }
        normalized_docs.append(normalized_doc)
    
    return normalized_docs


@router.put("/contact/{contact_id}")
async def update_contact(contact_id: str, data: ContactCreate, db=Depends(get_db)):
    """
    Update a contact by ID.
    """
    try:
        # Validate ObjectId
        object_id = ObjectId(contact_id)
        
        # Update the contact
        result = await db["contacts"].update_one(
            {"_id": object_id},
            {
                "$set": {
                    "first_name": data.first_name,
                    "last_name": data.last_name,
                    "email": data.email,
                    "phone_number": data.phone_number,
                    "message": data.message,
                    "services": data.services,
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        return {"message": "Contact updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid contact ID: {str(e)}")


@router.delete("/contact/{contact_id}")
async def delete_contact(contact_id: str, db=Depends(get_db)):
    """
    Delete a contact by ID.
    """
    try:
        # Validate ObjectId
        object_id = ObjectId(contact_id)
        
        # Delete the contact
        result = await db["contacts"].delete_one({"_id": object_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        return {"message": "Contact deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid contact ID: {str(e)}")
