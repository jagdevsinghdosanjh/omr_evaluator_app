import streamlit as st
from modules import omr_scanner, answer_comparator, result_generator
import os

st.title("📷 Scan OMR Sheet")

# --- Role Check ---
if st.session_state.get("user_role", "").lower() not in ["evaluator", "admin"]:
    st.warning("🚫 Access restricted to evaluators and admins.")
    st.stop()

# --- Upload OMR Sheet ---
uploaded_file = st.file_uploader("Upload scanned OMR sheet (JPG/PNG)", type=["jpg", "jpeg", "png"])

# --- Select Subject and Set ---
subject = st.selectbox("Select subject", ["Hindi", "English", "Math", "Science", "Social Studies", "Punjabi"])
set_number = st.selectbox("Select question set", ["Set 1", "Set 2", "Set 3"])

# --- Process and Compare ---
if uploaded_file and subject and set_number:
    st.image(uploaded_file, caption="Uploaded OMR Sheet", use_column_width=True)

    if st.button("🧩 Process and Compare"):
        try:
            # Step 1: Detect answers from image
            detected_answers = omr_scanner.extract_answers(uploaded_file)

            if not detected_answers:
                st.error("No answers detected. Please check the scan quality or alignment.")
                st.stop()

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

            # Step 4: Optional PDF Download
            if st.button("📥 Download Result PDF"):
                pdf_bytes = result_generator.generate_pdf(summary, subject, set_number)
                st.download_button("Download PDF", data=pdf_bytes, file_name="result.pdf", mime="application/pdf")

        except ValueError as ve:
            st.error(f"OMR processing error: {ve}")
        except Exception as e:
            st.error("Unexpected error during OMR processing.")
            st.text(f"Debug info: {e}")
