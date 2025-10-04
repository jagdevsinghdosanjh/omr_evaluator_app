import streamlit as st
from PIL import Image
import os

st.title("🌟 Constellation Badge Reveal")

# Role check
if st.session_state.get("user_role") != "Student":
    st.warning("Access restricted to students.")
    st.stop()

# Poetic intro
st.markdown("""
<div style="text-align:center; font-style:italic; color:#555; margin-bottom:2em;">
"Each scan is a spark. Each remix, a ripple. Each badge, a beacon in your learning sky."
</div>
""", unsafe_allow_html=True)

# Select badge type
badge_type = st.selectbox("Choose your badge constellation:", [
    "🧠 Quantum Thinker",
    "🎨 Remix Architect",
    "📜 Wisdom Wall Contributor",
    "🔍 OMR Explorer",
    "🌌 Showcase Star"
])

# Reveal animation (simulated)
if st.button("✨ Reveal My Badge"):
    st.success(f"Congratulations! You've earned the **{badge_type}** badge.")
    badge_path = f"assets/badges/{badge_type.split()[1].lower()}_badge.png"
    if os.path.exists(badge_path):
        st.image(Image.open(badge_path), caption=badge_type, use_column_width=True)
    else:
        st.info("Badge image coming soon...")

# Remix lineage (optional)
st.subheader("🔗 Remix Lineage")
st.markdown("""
Your badge is part of a remix constellation—linked to peers, mentors, and classroom creativity.
""")

# Simulated lineage map
st.markdown("""
- 🧠 You remixed a Math OMR scan from **Aarav**
- 🎨 Your badge inspired a showcase by **Meher**
- 🌌 Your constellation includes **3 remix stars** and **2 showcase echoes**
""")

# Optional download
if st.button("📥 Download Badge Certificate"):
    st.info("Download feature coming soon. Ask your evaluator for a printed copy.")
