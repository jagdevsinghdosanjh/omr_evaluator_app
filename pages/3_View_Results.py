import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Validate credentials
def validate_email_credentials():
    missing = []
    if not EMAIL_HOST:
        missing.append("EMAIL_HOST")
    if not EMAIL_PORT:
        missing.append("EMAIL_PORT")
    if not EMAIL_USER:
        missing.append("EMAIL_USER")
    if not EMAIL_PASS:
        missing.append("EMAIL_PASS")
    if missing:
        raise ValueError(f"❌ Missing email credentials: {', '.join(missing)}")

# Send result PDF via email
def send_result_email(recipient_email, student_name, subject, set_number, pdf_bytes):
    try:
        validate_email_credentials()
        port = int(EMAIL_PORT)

        msg = EmailMessage()
        msg["Subject"] = f"OMR Result for {student_name} - {subject} ({set_number})"
        msg["From"] = EMAIL_USER
        msg["To"] = recipient_email

        msg.set_content(
            f"""Hello {student_name},

Attached is your result for the {subject} ({set_number}) OMR evaluation.

Score: Please refer to the attached PDF for details.

Best regards,
OMR Evaluation Team"""
        )

        msg.add_attachment(
            pdf_bytes,
            maintype="application",
            subtype="pdf",
            filename="OMR_Result.pdf"
        )

        server = smtplib.SMTP(EMAIL_HOST, port)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        st.success(f"📧 Result sent to {recipient_email}")

    except Exception as e:
        st.error("Failed to send email. Please check credentials or network.")
        print(f"Email dispatch error: {e}")
