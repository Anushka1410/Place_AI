
import sqlite3
from pathlib import Path

# Store the database in the same folder as this file.
DATABASE_PATH = Path(__file__).parent / "placeai_tracker.db"


def get_connection():
    """Open a connection to the PlaceAI tracker database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the daily preparation table if it doesn't exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS daily_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_date TEXT NOT NULL,
                task_name TEXT NOT NULL,
                study_minutes INTEGER NOT NULL DEFAULT 0,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


if __name__ == "__main__":
    initialize_database()
    print("PlaceAI daily tracker database initialized successfully!")
