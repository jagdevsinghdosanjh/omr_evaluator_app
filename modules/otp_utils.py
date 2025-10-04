import random
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from twilio.rest import Client
from datetime import datetime, timedelta
import streamlit as st

load_dotenv()

# Email config
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Twilio config
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

# OTP expiry
OTP_EXPIRY_MINUTES = int(os.getenv("OTP_EXPIRY_MINUTES", 5))

# Generate 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP via email
def send_otp_email(recipient_email, otp):
    msg = EmailMessage()
    msg["Subject"] = "Your OTP for OMR App"
    msg["From"] = EMAIL_USER
    msg["To"] = recipient_email
    msg.set_content(f"Your OTP is: {otp}\nIt will expire in {OTP_EXPIRY_MINUTES} minutes.")

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

# Send OTP via SMS
from twilio.rest import Client
import streamlit as st

def send_otp_sms(recipient_mobile: str, otp: str):
    try:
        client = Client(st.secrets["TWILIO_ACCOUNT_SID"], st.secrets["TWILIO_AUTH_TOKEN"])
        sender = st.secrets["TWILIO_PHONE_NUMBER"]

        # Ensure E.164 format
        if not recipient_mobile.startswith("+"):
            recipient_mobile = "+91" + recipient_mobile.strip()

        message = client.messages.create(
            body=f"Your OTP for OMR App is: {otp}",
            from_=sender,
            to=recipient_mobile
        )
    except Exception as e:
        print(f"❌ Twilio SMS error: {e}")
        st.error("SMS delivery failed. Please use email login or verify your number in Twilio.")

# def send_otp_sms(recipient_mobile, otp):
#     client = Client(TWILIO_SID, TWILIO_TOKEN)
#     message = client.messages.create(
#         body=f"Your OTP for OMR App is: {otp}",
#         from_=TWILIO_PHONE,
#         to=recipient_mobile
#     )
#     return message.sid

# Store OTP in session
def store_otp(session, otp):
    session["otp"] = otp
    session["otp_expiry"] = datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)

# Verify OTP
def verify_otp(session, entered_otp):
    if "otp" not in session or "otp_expiry" not in session:
        return False
    if datetime.now() > session["otp_expiry"]:
        return False
    return entered_otp == session["otp"]
