from pydantic import BaseModel, EmailStr
from typing import Optional

class UserInDB(BaseModel):
    id: Optional[str]
    email: EmailStr
    hashed_password: str