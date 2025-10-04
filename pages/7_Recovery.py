import streamlit as st
from modules import otp_utils, auth
from utils.session_state import init_session

init_session()
st.title("🔐 Recover Your Password")

# Poetic reassurance
st.markdown("""
<div style="font-style:italic; color:#555; margin-bottom:1em;">
"Even stars forget their path. Let us help you realign your orbit."
</div>
""", unsafe_allow_html=True)

# Step 1: Identify user
identifier = st.text_input("Enter your registered email or mobile")

if st.button("📩 Send OTP") and identifier:
    otp = otp_utils.generate_otp()
    otp_utils.store_otp(st.session_state, otp)
    try:
        if "@" in identifier:
            otp_utils.send_otp_email(identifier, otp)
            st.success("OTP sent to your email.")
        else:
            otp_utils.send_otp_sms(identifier, otp)
            st.success("OTP sent to your mobile.")
    except Exception as e:
        st.error(f"Failed to send OTP: {e}")

# Step 2: Verify OTP
entered_otp = st.text_input("Enter the OTP you received")
if st.button("✅ Verify OTP"):
    if otp_utils.verify_otp(st.session_state, entered_otp):
        st.session_state["otp_verified"] = True
        st.success("OTP verified. You may now reset your password.")
    else:
        st.error("Invalid or expired OTP.")

# Step 3: Reset password
if st.session_state.get("otp_verified"):
    new_password = st.text_input("New password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    if st.button("🔁 Reset Password"):
        if new_password == confirm_password and len(new_password) >= 6:
            try:
                user = auth.get_user(identifier)
                if user:
                    auth.update_password(user_id=user[0], new_password=new_password)
                    st.success("🎉 Password reset successfully. You may now log in.")
                else:
                    st.error("User not found.")
            except Exception as e:
                st.error(f"Database error: {e}")
        else:
            st.error("Passwords do not match or are too short.")
