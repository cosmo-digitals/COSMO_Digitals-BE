from dataclasses import dataclass
from typing import Optional
from email_validator import validate_email, EmailNotValidError

@dataclass
class UserInDB:
    id: Optional[str]
    email: str
    hashed_password: str

    def __post_init__(self):
        if self.email:
            try:
                validate_email(self.email)
            except EmailNotValidError:
                raise ValueError("Invalid email format")