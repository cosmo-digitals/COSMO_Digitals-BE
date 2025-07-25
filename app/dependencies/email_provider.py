# app/dependencies/email_provider.py
from app.utils.email_utils import EmailSender

# Create one global instance to reuse across the app
email_sender = EmailSender()
