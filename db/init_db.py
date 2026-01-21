import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "finance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT CHECK(type IN ('income', 'expense', 'saving')) NOT NULL,
        category TEXT NOT NULL,
        sub_category TEXT,
        description TEXT NOT NULL,
        confidence REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")

if __name__ == "__main__":
    init_db()
