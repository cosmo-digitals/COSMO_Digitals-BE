import os
from email.message import EmailMessage
from typing import Any, Dict

from aiosmtplib import send
from dotenv import load_dotenv

load_dotenv()


async def send_contact_email(data: Dict[str, Any]) -> None:
    """
    Send an email notification for a contact-form submission.

    Args:
        data: Dictionary with keys
              - first_name
              - last_name
              - email
              - phone_number
              - message
    Raises:
        EnvironmentError: If any mandatory SMTP settings are missing.
    """
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", 587))
    smtp_user: str | None = os.getenv("SMTP_USERNAME")
    smtp_pass: str | None = os.getenv("SMTP_PASSWORD")
    notify_email: str | None = os.getenv("NOTIFY_EMAIL")
    from_email: str = os.getenv("DEFAULT_FROM_EMAIL", smtp_user or "")

    if not all([smtp_user, smtp_pass, notify_email]):
        raise EnvironmentError(
            "Please set SMTP_USERNAME, SMTP_PASSWORD and NOTIFY_EMAIL in your environment."
        )

    message = EmailMessage()
    message["From"] = from_email
    message["To"] = notify_email
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

    await send(
        message,
        hostname=smtp_host,
        port=smtp_port,
        start_tls=True,
        username=smtp_user,
        password=smtp_pass,
    )
