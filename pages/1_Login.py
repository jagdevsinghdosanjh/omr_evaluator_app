import streamlit as st
from modules import auth, otp_utils
from datetime import datetime  # noqa

st.title("🔐 Login to OMR Evaluator")

# Session init
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Login method
login_method = st.radio("Choose login method:", ["Mobile/Email + OTP", "Username + Password"])

def route_user_by_role(role):
    if role == "admin":
        st.success("🔗 Redirecting to Admin Dashboard...")
        st.markdown("[🧠 Go to Admin Dashboard](./4_Admin_Dashboard)")
    elif role == "educator":
        st.success("🔗 Educator access granted.")
        st.markdown("[📚 Go to Educator Panel](./3_Educator_Home)")
    elif role == "student":
        st.success("🔗 Student access granted.")
        st.markdown("[📝 Go to Student Portal](./5_Student_Home)")
    else:
        st.warning("Unknown role. Please contact support.")

if login_method == "Mobile/Email + OTP":
    identifier = st.text_input("Enter your registered mobile or email")

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
            st.warning("OTP delivery failed. Please verify your number or try email login.")
            print(f"OTP send error: {e}")

    entered_otp = st.text_input("Enter OTP")
    if st.button("✅ Verify OTP") and entered_otp:
        if otp_utils.verify_otp(st.session_state, entered_otp):
            try:
                user = auth.get_user(identifier)
                if user:
                    st.session_state.user_role = user[5].lower()
                    st.session_state.user_name = user[1]
                    st.success(f"Welcome {user[1]}! Logged in as {user[5]}")
                    route_user_by_role(user[5].lower())
                else:
                    st.error("User not found.")
            except Exception as e:
                st.error("Database error during login.")
                print(f"Login error: {e}")
        else:
            st.error("Invalid or expired OTP.")

else:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("🔐 Login") and username and password:
        try:
            user = auth.get_user(username)
            if user and auth.verify_password(password, user[4]):
                st.session_state.user_role = user[5].lower()
                st.session_state.user_name = user[1]
                st.success(f"Welcome {user[1]}! Logged in as {user[5]}")
                route_user_by_role(user[5].lower())
            else:
                st.error("Invalid credentials.")
        except Exception as e:
            st.error("Login failed due to system error.")
            print(f"Password login error: {e}")

# import streamlit as st
# from modules import auth, otp_utils
# from datetime import datetime # noqa

# st.title("🔐 Login to OMR Evaluator")

# # Session init
# if "user_role" not in st.session_state:
#     st.session_state.user_role = None
# if "user_name" not in st.session_state:
#     st.session_state.user_name = None

# # Login method
# login_method = st.radio("Choose login method:", ["Mobile/Email + OTP", "Username + Password"])

# if login_method == "Mobile/Email + OTP":
#     identifier = st.text_input("Enter your registered mobile or email")

#     if st.button("📩 Send OTP") and identifier:
#         otp = otp_utils.generate_otp()
#         otp_utils.store_otp(st.session_state, otp)

#         try:
#             if "@" in identifier:
#                 otp_utils.send_otp_email(identifier, otp)
#                 st.success("OTP sent to your email.")
#             else:
#                 otp_utils.send_otp_sms(identifier, otp)
#                 st.success("OTP sent to your mobile.")
#         except Exception as e:
#             st.warning("OTP delivery failed. Please verify your number or try email login.")
#             print(f"OTP send error: {e}")

#     entered_otp = st.text_input("Enter OTP")
#     if st.button("✅ Verify OTP") and entered_otp:
#         if otp_utils.verify_otp(st.session_state, entered_otp):
#             try:
#                 user = auth.get_user(identifier)
#                 if user:
#                     st.session_state.user_role = user[5]
#                     st.session_state.user_name = user[1]
#                     st.success(f"Welcome {user[1]}! Logged in as {user[5]}")
#                 else:
#                     st.error("User not found.")
#             except Exception as e:
#                 st.error("Database error during login.")
#                 print(f"Login error: {e}")
#         else:
#             st.error("Invalid or expired OTP.")

# else:
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("🔐 Login") and username and password:
#         try:
#             user = auth.get_user(username)
#             if user and auth.verify_password(password, user[4]):
#                 st.session_state.user_role = user[5]
#                 st.session_state.user_name = user[1]
#                 st.success(f"Welcome {user[1]}! Logged in as {user[5]}")
#             else:
#                 st.error("Invalid credentials.")
#         except Exception as e:
#             st.error("Login failed due to system error.")
#             print(f"Password login error: {e}")