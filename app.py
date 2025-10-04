import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="OMR Evaluator", layout="wide")

st.title("📄 OMR Evaluation App")
st.write("Scan, compare, and generate instant results for multiple-choice exams.")

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if st.session_state.user_role:
    st.success(f"Logged in as {st.session_state.user_role}")
else:
    st.info("Please log in to continue.")
