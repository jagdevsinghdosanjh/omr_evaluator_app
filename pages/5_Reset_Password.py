import streamlit as st
from modules import auth, otp_utils

st.title("🔁 Reset Your Password")

# Step 1: Identify user
identifier = st.text_input("Enter your registered mobile or email")

if st.button("Send OTP"):
    otp = otp_utils.generate_otp()
    otp_utils.store_otp(st.session_state, otp)
    if "@" in identifier:
        otp_utils.send_otp_email(identifier, otp)
        st.success("OTP sent to your email.")
    else:
        otp_utils.send_otp_sms(identifier, otp)
        st.success("OTP sent to your mobile.")

# Step 2: Verify OTP
entered_otp = st.text_input("Enter OTP")
if st.button("Verify OTP"):
    if otp_utils.verify_otp(st.session_state, entered_otp):
        st.session_state["otp_verified"] = True
        st.success("OTP verified. You may now reset your password.")
    else:
        st.error("Invalid or expired OTP.")

# Step 3: Reset password
if st.session_state.get("otp_verified"):
    new_password = st.text_input("Enter new password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")
    if st.button("Reset Password"):
        if new_password == confirm_password and len(new_password) >= 6:
            user = auth.get_user(identifier)
            if user:
                auth.update_password(user_id=user[0], new_password=new_password)
                st.success("✅ Password reset successfully. You may now log in.")
            else:
                st.error("User not found.")
        else:
            st.error("Passwords do not match or are too short.")
