
import json
import sqlite3
import os

# Path to the Cowrie JSON log
LOG_FILE = "logs/cowrie/cowrie.json"

# SQLite database
DB_FILE = "database/honeypot.db"

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    eventid TEXT,
    src_ip TEXT,
    username TEXT,
    password TEXT,
    command TEXT
)
""")

with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            data = json.loads(line)

            timestamp = data.get("timestamp", "")
            eventid = data.get("eventid", "")
            src_ip = data.get("src_ip", "")
            username = data.get("username", "")
            password = data.get("password", "")
            command = data.get("input", "")

            cursor.execute("""
                INSERT INTO attacks
                (timestamp,eventid,src_ip,username,password,command)
                VALUES (?,?,?,?,?,?)
            """, (
                timestamp,
                eventid,
                src_ip,
                username,
                password,
                command
            ))

        except Exception:
            pass

conn.commit()
conn.close()

print("Logs imported successfully!")