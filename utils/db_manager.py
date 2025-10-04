import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "data/logs.db")

# Connect to DB
def get_connection():
    return sqlite3.connect(DB_PATH)

# Initialize users table
def initialize_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            mobile TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize logs table
def initialize_logs_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            evaluator_name TEXT,
            evaluator_id TEXT,
            subject TEXT,
            set_number TEXT,
            score TEXT,
            pdf_generated TEXT,
            pdf_sent TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize all tables
def initialize_all():
    initialize_users_table()
    initialize_logs_table()
