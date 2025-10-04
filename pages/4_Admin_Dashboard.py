import streamlit as st
from modules import logger
import os
import json

st.title("🧠 Admin Dashboard")

# Role check
if st.session_state.get("user_role") != "Admin":
    st.warning("Access restricted to administrators.")
    st.stop()

# Section: View Logs
st.subheader("📋 Session Logs")
logs = logger.get_logs()
if logs:
    st.dataframe(logs, use_container_width=True)
else:
    st.info("No logs found.")

# Section: Upload Answer Keys
st.subheader("📤 Upload Answer Key")
subject = st.selectbox("Subject", ["Hindi", "English", "Math", "Science", "Social Studies", "Punjabi"])
set_number = st.selectbox("Set", ["Set 1", "Set 2", "Set 3"])
uploaded_key = st.file_uploader("Upload answer key (JSON format)", type=["json"])

if uploaded_key and st.button("Save Answer Key"):
    save_path = f"data/answer_keys/{subject.lower()}_{set_number.lower()}.json"
    with open(save_path, "wb") as f:
        f.write(uploaded_key.getvalue())
    st.success(f"Answer key saved for {subject} - {set_number}")

# Section: View Existing Keys
st.subheader("📚 Existing Answer Keys")
key_files = os.listdir("data/answer_keys")
for key_file in key_files:
    st.markdown(f"- {key_file}")
    with open(f"data/answer_keys/{key_file}", "r") as f:
        key_data = json.load(f)
        st.json(key_data)

# Section: User Management (Optional)
st.subheader("👥 User Management")
st.info("User creation and editing can be added here in future iterations.")
