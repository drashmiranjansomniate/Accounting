import random

from datetime import datetime, timedelta

from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig
)

from app.core.config import settings


otp_storage = {}

verified_emails = {}


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


def generate_otp():

    return str(random.randint(100000, 999999))


def store_otp(
    email: str,
    otp: str
):

    otp_storage[email] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=10)
    }


async def send_otp_email(
    email: str
):

    otp = generate_otp()

    store_otp(email, otp)

    message = MessageSchema(
        subject="OTP Verification",
        recipients=[email],
        body=f"Your OTP is: {otp}",
        subtype="plain"
    )

    fm = FastMail(conf)

    await fm.send_message(message)


def verify_otp(
    email: str,
    otp: str
):

    data = otp_storage.get(email)

    if not data:
        return False

    if datetime.utcnow() > data["expires_at"]:
        del otp_storage[email]
        return False

    if data["otp"] != otp:
        return False

    verified_emails[email] = {
        "verified": True,
        "expires_at": datetime.utcnow() + timedelta(minutes=10)
    }

    del otp_storage[email]

    return True


def is_email_verified(
    email: str
):

    data = verified_emails.get(email)

    if not data:
        return False

    if datetime.utcnow() > data["expires_at"]:
        del verified_emails[email]
        return False

    return True