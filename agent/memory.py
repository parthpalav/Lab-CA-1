import os
import sqlite3
from datetime import datetime, timezone


class Memory:
    def __init__(self, db_path="logs/agent_history.db"):
        self.history = []
        self.document = ""
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS message_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    action TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add(self, user_input):
        self.history.append(user_input)

    def set_document(self, text):
        self.document = text

    def add_message(self, role, content, action=None):
        timestamp = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO message_logs (role, content, action, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (role, str(content), action, timestamp),
            )
            conn.commit()