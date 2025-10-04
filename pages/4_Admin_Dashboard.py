import streamlit as st
from modules import logger, auth
import os
import json
import uuid
from email_validator import validate_email, EmailNotValidError
import pandas as pd

st.title("🧠 Admin Dashboard")

# Role check
if st.session_state.get("user_role") != "admin":
    st.warning("🚫 Access restricted to administrators.")
    st.stop()

# Poetic welcome
st.markdown("""
<div style="font-style:italic; color:#555; margin-bottom:1em;">
"Welcome, Commander of the Evaluator Constellation. Your tools await."
</div>
""", unsafe_allow_html=True)

# 📋 Session Logs
st.subheader("📋 Session Logs")
logs = logger.get_logs()
if logs:
    st.dataframe(logs, use_container_width=True)
else:
    st.info("No logs found.")

# 📤 Upload Answer Key
st.subheader("📤 Upload Answer Key")
subject = st.selectbox("Subject", ["Hindi", "English", "Math", "Science", "Social Studies", "Punjabi"])
set_number = st.selectbox("Set", ["Set 1", "Set 2", "Set 3"])
uploaded_key = st.file_uploader("Upload answer key (JSON format)", type=["json"])

if uploaded_key and st.button("💾 Save Answer Key"):
    save_path = f"data/answer_keys/{subject.lower()}_{set_number.lower()}.json"
    with open(save_path, "wb") as f:
        f.write(uploaded_key.getvalue())
    st.success(f"✅ Answer key saved for {subject} - {set_number}")

# 📚 View Existing Answer Keys
st.subheader("📚 Existing Answer Keys")
key_files = os.listdir("data/answer_keys")
for key_file in key_files:
    st.markdown(f"- `{key_file}`")
    with open(f"data/answer_keys/{key_file}", "r") as f:
        key_data = json.load(f)
        st.json(key_data)

st.subheader("📊 Filter Logs")

# Load logs
logs = logger.get_logs()
if logs:
    columns = [
        "ID", "Timestamp", "Evaluator Name", "Evaluator ID",
        "Subject", "Set Number", "Score", "PDF Generated", "PDF Sent"
    ]
    df = pd.DataFrame(logs, columns=columns)

    # Filters
    with st.expander("🔍 Filter Options"):
        subject_filter = st.multiselect("Subject", df["Subject"].unique())
        evaluator_filter = st.multiselect("Evaluator", df["Evaluator Name"].unique())
        date_range = st.date_input("Date Range", [])

        filtered_df = df.copy()

        if subject_filter:
            filtered_df = filtered_df[filtered_df["Subject"].isin(subject_filter)]
        if evaluator_filter:
            filtered_df = filtered_df[filtered_df["Evaluator Name"].isin(evaluator_filter)]
        if len(date_range) == 2:
            start, end = [d.strftime("%Y-%m-%d") for d in date_range]
            filtered_df = filtered_df[
                filtered_df["Timestamp"].str[:10].between(start, end)
            ]

    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("No logs found.")


# 👥 User Management
st.subheader("👥 Register New User")

new_name = st.text_input("Full Name")
new_mobile = st.text_input("Mobile Number")
new_email = st.text_input("Email Address")
new_password = st.text_input("Create Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")
new_role = st.selectbox("Role", ["student", "educator", "admin"])

if st.button("➕ Register User"):
    if not all([new_name, new_mobile, new_email, new_password, confirm_password]):
        st.error("Please fill in all fields.")
    elif new_password != confirm_password:
        st.error("Passwords do not match.")
    elif len(new_password) < 6:
        st.error("Password must be at least 6 characters.")
    else:
        try:
            validate_email(new_email)
            user_id = str(uuid.uuid4())
            auth.create_user(user_id, new_name, new_mobile, new_email, new_password, new_role)
            st.success(f"🎉 {new_role.capitalize()} '{new_name}' registered successfully.")
        except EmailNotValidError:
            st.error("Invalid email format.")
        except Exception as e:
            st.error("Registration failed. Please check inputs or database.")
            print(f"Admin registration error: {e}")

# import streamlit as st
# from modules import logger
# import os
# import json

# st.title("🧠 Admin Dashboard")

# # Role check
# if st.session_state.get("user_role") != "Admin":
#     st.warning("Access restricted to administrators.")
#     st.stop()

# # Section: View Logs
# st.subheader("📋 Session Logs")
# logs = logger.get_logs()
# if logs:
#     st.dataframe(logs, use_container_width=True)
# else:
#     st.info("No logs found.")

# # Section: Upload Answer Keys
# st.subheader("📤 Upload Answer Key")
# subject = st.selectbox("Subject", ["Hindi", "English", "Math", "Science", "Social Studies", "Punjabi"])
# set_number = st.selectbox("Set", ["Set 1", "Set 2", "Set 3"])
# uploaded_key = st.file_uploader("Upload answer key (JSON format)", type=["json"])

# if uploaded_key and st.button("Save Answer Key"):
#     save_path = f"data/answer_keys/{subject.lower()}_{set_number.lower()}.json"
#     with open(save_path, "wb") as f:
#         f.write(uploaded_key.getvalue())
#     st.success(f"Answer key saved for {subject} - {set_number}")

# # Section: View Existing Keys
# st.subheader("📚 Existing Answer Keys")
# key_files = os.listdir("data/answer_keys")
# for key_file in key_files:
#     st.markdown(f"- {key_file}")
#     with open(f"data/answer_keys/{key_file}", "r") as f:
#         key_data = json.load(f)
#         st.json(key_data)

# # Section: User Management (Optional)
# st.subheader("👥 User Management")
# st.info("User creation and editing can be added here in future iterations.")
