from fastapi import APIRouter, HTTPException, status, Depends, Request
from dataclasses import dataclass
from typing import Any
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

from app.database.mongodb import get_db
from app.dependencies.email_provider import email_sender  # Global email sender

router = APIRouter(tags=["public-contact"])


@dataclass
class ContactForm:
    first_name: str
    last_name: str
    email: str
    phone_number: str
    message: str
    services: list[str] = None

    def __post_init__(self):
        if self.services is None:
            self.services = []
        
        # Validation
        if not self.first_name:
            raise ValueError("First name is required")
        
        if not self.last_name:
            raise ValueError("Last name is required")
        
        if not self.email:
            raise ValueError("Email is required")
        
        # Validate email format
        try:
            validate_email(self.email)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        
        if not self.phone_number:
            raise ValueError("Phone number is required")
        
        if not self.message:
            raise ValueError("Message is required")

    def dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "message": self.message,
            "services": self.services
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email", ""),
            phone_number=data.get("phone_number", ""),
            message=data.get("message", ""),
            services=data.get("services", [])
        )


@router.post("/contact/", status_code=status.HTTP_201_CREATED)
async def submit_contact(request: Request, db=Depends(get_db)):
    try:
        # Parse JSON body manually
        body = await request.json()
        
        # Create ContactForm instance
        form = ContactForm.from_dict(body)
        
        print("✅ Form data received:")
        print(form.dict())  # DEBUG: Show received form data

        contact_data: dict[str, Any] = form.dict()
        contact_data["created_at"] = datetime.utcnow()

        print("📦 Inserting into MongoDB...")
        result = await db["contacts"].insert_one(contact_data)
        print(f"🟢 Saved to DB. ID: {result.inserted_id}")

        print("📤 Sending email...")
        await email_sender.send_contact_email(contact_data)
        print("✅ Email sent successfully.")

        return {
            "message": "Contact saved and email sent successfully.",
            "id": str(result.inserted_id),
        }

    except ValueError as ve:
        print(f"❌ Validation error: {ve}")
        raise HTTPException(
            status_code=400, detail=f"Validation error: {ve}"
        )
    except Exception as exc:
        print("❌ Error occurred during contact form processing:")
        print(exc)  # DEBUG: Print the full error to console
        raise HTTPException(
            status_code=500, detail=f"Failed to save or send email: {exc}"
        )
