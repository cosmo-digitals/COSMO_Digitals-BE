# app/utils/email_utils.py
import os
from email.message import EmailMessage
from typing import Any, Dict
from aiosmtplib import SMTP
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USERNAME")
        self.smtp_pass = os.getenv("SMTP_PASSWORD")
        self.notify_email = os.getenv("NOTIFY_EMAIL")
        self.from_email = os.getenv("DEFAULT_FROM_EMAIL", self.smtp_user or "")

        if not all([self.smtp_user, self.smtp_pass, self.notify_email]):
            raise EnvironmentError(
                "Please set SMTP_USERNAME, SMTP_PASSWORD, and NOTIFY_EMAIL in your environment."
            )

        self.smtp_client = SMTP(
            hostname=self.smtp_host,
            port=self.smtp_port,
            start_tls=False,
        )

    async def connect(self):
        if not self.smtp_client.is_connected:
            await self.smtp_client.connect()
            await self.smtp_client.starttls()
            await self.smtp_client.login(self.smtp_user, self.smtp_pass)

    async def send_contact_email(self, data: Dict[str, Any]) -> None:
        await self.connect()

        message = EmailMessage()
        message["From"] = self.from_email
        message["To"] = self.notify_email
        message["Subject"] = (
            f"New Contact Form Submission from {data['first_name']} {data['last_name']}"
        )

        body = (
            "✅ You have a new contact form submission!\n\n"
            f"📌 Full Name: {data['first_name']} {data['last_name']}\n"
            f"📧 Email: {data['email']}\n"
            f"📱 Phone: {data['phone_number']}\n"
            "💬 Message:\n"
            f"{data['message']}"
        )
        message.set_content(body)

        await self.smtp_client.send_message(message)
