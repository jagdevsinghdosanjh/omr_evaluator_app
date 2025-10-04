import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "data/logs.db")

# Ensure logs table exists
def initialize_logs_table():
    conn = sqlite3.connect(DB_PATH)
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

# Log a session entry
def log_session(evaluator_name, evaluator_id, subject, set_number, score, pdf_generated="No", pdf_sent="No"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO logs (timestamp, evaluator_name, evaluator_id, subject, set_number, score, pdf_generated, pdf_sent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, evaluator_name, evaluator_id, subject, set_number, score, pdf_generated, pdf_sent))
    conn.commit()
    conn.close()

# Retrieve logs (optional for dashboard)
def get_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
