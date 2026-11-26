import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent / "expenses.db"

CATEGORIES = {
    "Expense": [
        "Food", "Transport", "Shopping", "Bills", "Education",
        "Health", "Entertainment", "Travel", "Other"
    ],
    "Income": ["Salary", "Freelance", "Business", "Gift", "Other"]
}

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL CHECK(kind IN ('Income', 'Expense')),
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                transaction_date TEXT NOT NULL
            )
        """)
        conn.commit()

def add_transaction(kind, category, description, amount, transaction_date):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO transactions
               (kind, category, description, amount, transaction_date)
               VALUES (?, ?, ?, ?, ?)""",
            (kind, category, description, amount, transaction_date)
        )
        conn.commit()

def get_transactions():
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT id, kind, category, description, amount, transaction_date
               FROM transactions ORDER BY transaction_date DESC, id DESC"""
        ).fetchall()
    return pd.DataFrame([dict(row) for row in rows],
                        columns=["id", "kind", "category", "description", "amount", "transaction_date"])

def update_transaction(transaction_id, kind, category, description, amount, transaction_date):
    with get_connection() as conn:
        conn.execute(
            """UPDATE transactions
               SET kind=?, category=?, description=?, amount=?, transaction_date=?
               WHERE id=?""",
            (kind, category, description, amount, transaction_date, transaction_id)
        )
        conn.commit()

def delete_transaction(transaction_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        conn.commit()

def get_categories(kind):
    return CATEGORIES[kind]
