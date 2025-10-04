import sqlite3

def initialize_database(db_path="data/logs.db"):
    conn = sqlite3.connect(db_path)
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

if __name__ == "__main__":
    initialize_database()
    print("✅ Database initialized with 'users' table.")

# import sqlite3

# def initialize_database(db_path="data/logs.db"):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         user_id TEXT PRIMARY KEY,
#         name TEXT NOT NULL,
#         mobile TEXT UNIQUE,
#         email TEXT UNIQUE,
#         password_hash TEXT NOT NULL,
#         role TEXT NOT NULL
#     )
#     """)

#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     initialize_database()
#     print("✅ Database initialized with 'users' table.")
