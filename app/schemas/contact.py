from pydantic import BaseModel, EmailStr, Field

class ContactCreate(BaseModel):
    name: str = Field(..., max_length=80)
    email: EmailStr
    subject: str = Field(..., max_length=120)
    message: str = Field(..., max_length=2000)
