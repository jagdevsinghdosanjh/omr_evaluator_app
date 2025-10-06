import streamlit as st
import sqlite3
import pandas as pd
import os

# --- Config ---
DB_PATH = os.path.join("data", "logs.db")
ADMIN_CREDENTIALS = {
    "jagdevsinghdosanjh@gmail.com": "CF@12345"
}

# --- Login ---
def login():
    st.title("🔐 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if ADMIN_CREDENTIALS.get(username) == password:
            st.session_state["logged_in"] = True
            st.success(f"Welcome {username.split('@')[0].title()}! Logged in as admin.")
        else:
            st.error("Invalid credentials")

# --- Query Viewer ---
def display_query_results(query):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()

        df = pd.DataFrame(data, columns=columns)
        selected_columns = st.multiselect("Choose columns to display", columns, default=columns)
        st.dataframe(df[selected_columns], width=True)
        # st.dataframe(df[selected_columns], use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")

# --- Main ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        st.title("📊 Custom Query Viewer")
        query = st.text_area("Enter your SQL query", "SELECT * FROM users LIMIT 10")
        if st.button("Run Query"):
            display_query_results(query)
    else:
        login()

if __name__ == "__main__":
    main()
