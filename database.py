import sqlite3
from datetime import datetime, timezone

DB_PATH = "meetings.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            transcript TEXT NOT NULL,
            summary TEXT NOT NULL,
            action_items TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_meeting(user_id: int, transcript: str, summary: str, action_items: list[str]):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO meetings (user_id, transcript, summary, action_items, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            user_id,
            transcript,
            summary,
            "\n".join(action_items),
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()
