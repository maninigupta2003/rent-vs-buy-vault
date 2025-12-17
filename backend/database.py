# SQLite database + audit trail
import sqlite3
from datetime import datetime
from config import DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            payload TEXT,
            created_at TEXT
        )
    """)
    db.commit()

def log_event(event, payload):
    db = get_db()
    db.execute(
        "INSERT INTO audit_log (event, payload, created_at) VALUES (?, ?, ?)",
        (event, str(payload), datetime.utcnow().isoformat())
    )
    db.commit()
