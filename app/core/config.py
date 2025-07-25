import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    def __init__(self):
        self.mongo_uri = os.getenv("mongo_uri", "mongodb://localhost:27017")
        self.mongo_db_name = os.getenv("MONGO_DB_NAME", "my_fastapi_db")
        
        # Email settings
        self.smtp_host = os.getenv("smtp_host", "smtp.gmail.com")
        self.smtp_port = os.getenv("smtp_port", "587")
        self.smtp_username = os.getenv("smtp_username", "")
        self.smtp_password = os.getenv("smtp_password", "")
        self.smtp_use_tls = os.getenv("smtp_use_tls", "true")
        self.notify_email = os.getenv("notify_email", "")
        self.default_from_email = os.getenv("default_from_email", "")

settings = Settings()
