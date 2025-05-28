# db.py
import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create chat history table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        sender TEXT,
        message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def save_message(username, sender, message):
    cursor.execute(
        "INSERT INTO chat_history (username, sender, message) VALUES (?, ?, ?)",
        (username, sender, message)
    )
    conn.commit()

def load_chat_history(username):
    cursor.execute(
        "SELECT sender, message FROM chat_history WHERE username = ? ORDER BY timestamp",
        (username,)
    )
    return cursor.fetchall()
