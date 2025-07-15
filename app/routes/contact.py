from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.utils.email_utils import send_contact_email

router = APIRouter()

class ContactForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    message: str

@router.post("/contact/")
async def submit_contact(form: ContactForm):
    try:
        await send_contact_email(form.dict())
        return {"message": "Form submitted and email sent successfully."}
    except Exception as e:
        print("Email sending error:", e)
        raise HTTPException(status_code=500, detail="Failed to send email.")



