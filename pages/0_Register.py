import streamlit as st
import uuid
from modules import auth
from email_validator import validate_email, EmailNotValidError

st.title("📝 Register for OMR Evaluator")

# Poetic reassurance
st.markdown("""
<div style="font-style:italic; color:#555; margin-bottom:1em;">
"Every evaluator begins as a seeker. Welcome to your orbit."
</div>
""", unsafe_allow_html=True)

# Form inputs
name = st.text_input("Full Name")
mobile = st.text_input("Mobile Number")
email = st.text_input("Email Address")
password = st.text_input("Create Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")
role = st.selectbox("Role", ["student", "educator", "admin"])

# Submit button
if st.button("🚀 Register"):
    # Basic validation
    if not all([name, mobile, email, password, confirm_password]):
        st.error("Please fill in all fields.")
    elif password != confirm_password:
        st.error("Passwords do not match.")
    elif len(password) < 6:
        st.error("Password must be at least 6 characters.")
    else:
        try:
            validate_email(email)
            user_id = str(uuid.uuid4())
            auth.create_user(user_id, name, mobile, email, password, role)
            st.success("🎉 Registration successful! You may now log in.")
        except EmailNotValidError:
            st.error("Invalid email format.")
        except Exception as e:
            st.error("Registration failed. Please try again.")
            print(f"Registration error: {e}")
