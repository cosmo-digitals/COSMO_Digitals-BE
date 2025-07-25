from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError

@dataclass
class ContactBase:
    first_name: str
    last_name: str
    email: str
    phone_number: str
    message: str
    services: List[str] = None

    def __post_init__(self):
        if self.services is None:
            self.services = []
        
        # Validation
        if not self.first_name or len(self.first_name.strip()) < 1:
            raise ValueError("First name is required and must be at least 1 character")
        
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

@dataclass
class ContactCreate:
    """Schema used when a new contact comes in from the public form"""
    first_name: str
    last_name: str
    email: str
    phone_number: str
    message: str
    services: List[str] = None

    def __post_init__(self):
        if self.services is None:
            self.services = []
        
        # Validation
        if not self.first_name or len(self.first_name.strip()) < 1:
            raise ValueError("First name is required and must be at least 1 character")
        
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

@dataclass
class ContactInDB:
    """Schema returned by the API (contains an id string and timestamp)"""
    first_name: str
    last_name: str
    email: str
    phone_number: str
    message: str
    services: List[str] = None
    id: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.services is None:
            self.services = []
        
        # Validation
        if not self.first_name or len(self.first_name.strip()) < 1:
            raise ValueError("First name is required and must be at least 1 character")
        
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
