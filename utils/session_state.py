import streamlit as st

# Initialize session variables if not already set
def init_session():
    defaults = {
        "user_role": None,
        "user_name": None,
        "otp": None,
        "otp_expiry": None,
        "otp_verified": False,
        "scanned_answers": None,
        "result_summary": None,
        "pdf_ready": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Clear session after logout or reset
def clear_session():
    keys_to_clear = [
        "user_role", "user_name", "otp", "otp_expiry",
        "otp_verified", "scanned_answers", "result_summary", "pdf_ready"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
