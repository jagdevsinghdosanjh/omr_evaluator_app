import random
import time
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# OTP generation
def generate_otp():
    return str(random.randint(100000, 999999))

# Store OTP in session with expiry
def store_otp(session, otp, expiry_seconds=300):
    session["otp"] = otp
    session["otp_expiry"] = time.time() + expiry_seconds

# Verify OTP
def verify_otp(session, entered_otp):
    stored_otp = session.get("otp")
    expiry = session.get("otp_expiry", 0)
    if time.time() > expiry:
        return False
    return entered_otp == stored_otp

# Send OTP via email
def send_otp_email(recipient_email, otp):
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    msg = EmailMessage()
    msg["Subject"] = "Your OTP for Password Recovery"
    msg["From"] = EMAIL_USER
    msg["To"] = recipient_email
    msg.set_content(f"Your OTP is: {otp}\nIt will expire in 5 minutes.")

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

# Send OTP via SMS (placeholder)
def send_otp_sms(mobile_number, otp):
    print(f"Sending OTP {otp} to mobile {mobile_number} (SMS gateway integration pending)")
