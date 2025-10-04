import streamlit as st
from utils.session_state import init_session

init_session()

st.markdown("""
<div class="splash">
    <h1>🌠 Welcome to the Quantum Constellation</h1>
    <p>Where every bubble scanned becomes a star, every answer a ripple in the learning cosmos.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🧠 What You Can Do Here

- 🔐 **Login** as Student, Evaluator, or Admin
- 📷 **Scan OMR Sheets** and compare answers
- 📊 **View Results** and download PDFs
- 📧 **Send Results** via email
- 🧩 **Upload Answer Keys** and manage logs
- 🎓 **Celebrate Learning** with constellation badge maps and remix lineage

---

### ✨ Why This Matters

This isn’t just an app—it’s a stage for student pride, a toolkit for educator clarity, and a constellation of curiosity. Each scan is a story. Each result, a reflection. Each badge, a beacon.

Let’s begin.
""")

# Optional: Add a poetic footer
st.markdown("""
<div style='text-align:center; margin-top:3em; font-style:italic; color:#555;'>
"To evaluate is to illuminate. To reflect is to empower. To remix is to rise."
</div>
""", unsafe_allow_html=True)
