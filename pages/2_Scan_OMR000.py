import streamlit as st
from modules import omr_scanner, answer_comparator, result_generator
import os

st.title("📷 Scan OMR Sheet")

# Role check
if st.session_state.get("user_role", "").lower() not in ["evaluator", "admin"]:
    st.warning("🚫 Access restricted to evaluators and admins.")
    st.stop()

# if st.session_state.get("user_role") not in ["Evaluator", "Admin"]:
#     st.warning("Access restricted to evaluators and admins.")
#     st.stop()

# Upload OMR sheet
uploaded_file = st.file_uploader("Upload scanned OMR sheet (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Select subject and set
subject = st.selectbox("Select subject", ["Hindi", "English", "Math", "Science", "Social Studies", "Punjabi"])
set_number = st.selectbox("Select question set", ["Set 1", "Set 2", "Set 3"])

if uploaded_file and subject and set_number:
    st.image(uploaded_file, caption="Uploaded OMR Sheet", use_column_width=True)

    if st.button("🧩 Process and Compare"):
        # Step 1: Detect answers from image
        detected_answers = omr_scanner.extract_answers(uploaded_file)

        # Step 2: Load answer key
        answer_key_path = f"data/answer_keys/{subject.lower()}_{set_number.lower()}.json"
        if not os.path.exists(answer_key_path):
            st.error("Answer key not found.")
            st.stop()

        correct_answers = answer_comparator.load_answer_key(answer_key_path)

        # Step 3: Compare and generate result
        result = answer_comparator.compare_answers(detected_answers, correct_answers)
        summary = result_generator.generate_summary(result)

        st.success("✅ Result generated successfully.")
        st.write(summary)

        # Optional: download PDF
        if st.button("📥 Download Result PDF"):
            pdf_bytes = result_generator.generate_pdf(summary, subject, set_number)
            st.download_button("Download PDF", data=pdf_bytes, file_name="result.pdf", mime="application/pdf")
