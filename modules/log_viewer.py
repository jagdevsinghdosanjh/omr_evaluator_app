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

# --- Log Viewer ---
def show_logs():
    st.title("📜 Log Viewer")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if tables:
            selected_table = st.selectbox("Select Log Table", [t[0] for t in tables])

            # Fetch data and column names
            query = f"SELECT * FROM {selected_table} LIMIT 100"
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            # Create DataFrame with full column control
            df = pd.DataFrame(data, columns=columns)

            # Optional: Display column selector
            selected_columns = st.multiselect("Choose columns to display", columns, default=columns)
            st.dataframe(df[selected_columns], use_container_width=True)

        else:
            st.warning("No tables found in logs.db")

        conn.close()
    except Exception as e:
        st.error(f"Error loading logs: {e}")

# --- Main ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        show_logs()
    else:
        login()

if __name__ == "__main__":
    main()


# import streamlit as st
# import sqlite3

# # --- Config ---
# DB_PATH = "logs.db"
# ADMIN_CREDENTIALS = {
#     "jagdevsinghdosanjh@gmail.com": "CF@12345"
# }

# # --- Login ---
# def login():
#     st.title("🔐 Admin Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if ADMIN_CREDENTIALS.get(username) == password:
#             st.session_state["logged_in"] = True
#             st.success(f"Welcome {username.split('@')[0].title()}! Logged in as admin.")
#         else:
#             st.error("Invalid credentials")

# # --- Log Viewer ---
# def show_logs():
#     st.title("📜 Log Viewer")
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         cursor = conn.cursor()
#         cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#         tables = cursor.fetchall()

#         if tables:
#             selected_table = st.selectbox("Select Log Table", [t[0] for t in tables])
#             query = f"SELECT * FROM {selected_table} LIMIT 100"
#             data = cursor.execute(query).fetchall()
#             columns = [description[0] for description in cursor.description]
#             st.dataframe(data, use_container_width=True)
#         else:
#             st.warning("No tables found in logs.db")

#         conn.close()
#     except Exception as e:
#         st.error(f"Error loading logs: {e}")
        


# # --- Main ---
# def main():
#     if "logged_in" not in st.session_state:
#         st.session_state["logged_in"] = False

#     if st.session_state["logged_in"]:
#         show_logs()
#     else:
#         login()

# if __name__ == "__main__":
#     main()
