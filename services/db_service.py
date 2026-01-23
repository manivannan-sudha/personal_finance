import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parents[1] / "db" / "finance.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def insert_transaction(txn: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (date, amount, type, category, sub_category, description, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        txn["date"],
        txn["amount"],
        txn["type"],
        txn["category"],
        txn.get("sub_category"),
        txn["description"],
        txn.get("confidence")
    ))

    conn.commit()
    conn.close()


def fetch_recent_transactions(limit :int=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM transactions
        ORDER BY date DESC, id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows