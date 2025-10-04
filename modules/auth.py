import bcrypt
import sqlite3
import os
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError
from modules.db_initializer import initialize_database

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "data/logs.db")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def get_user(identifier: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, name, mobile, email, password_hash, role
        FROM users
        WHERE mobile = ? OR email = ?
    """, (identifier, identifier))
    user = cursor.fetchone()
    conn.close()
    return user

def update_password(user_id: str, new_password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed = hash_password(new_password)
    cursor.execute("""
        UPDATE users SET password_hash = ? WHERE user_id = ?
    """, (hashed, user_id))
    conn.commit()
    conn.close()

def create_user(user_id: str, name: str, mobile: str, email: str, password: str, role: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("""
        INSERT INTO users (user_id, name, mobile, email, password_hash, role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, name, mobile, email, hashed, role))
    conn.commit()
    conn.close()

def ensure_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        mobile TEXT UNIQUE,
        email TEXT UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# ✅ Initialize database and ensure table
initialize_database()
ensure_users_table()
