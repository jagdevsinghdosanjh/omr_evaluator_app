import sqlite3
conn = sqlite3.connect("data/logs.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
conn.close()
