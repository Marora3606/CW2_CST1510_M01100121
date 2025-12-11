"""Database Connection Module"""

import sqlite3
from pathlib import Path

# Resolve DB path relative to the package so the app works regardless of
# the current working directory (important when running via Streamlit)
DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "DATA" / "intelligence_platform.db"


def connect_database(db_path: Path = DEFAULT_DB_PATH):
    """Connect to SQLite database. Creates parent directories if needed.

    Ensures the parent DATA directory exists so sqlite can create journal/WAL
    files when opening the database.
    """
    db_path = Path(db_path)
    parent = db_path.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        raise sqlite3.OperationalError(f"Unable to create database directory: {parent}")

    return sqlite3.connect(str(db_path))



def close_database(conn):
    """Close the database connection safely."""
    if conn:
        conn.close()


if __name__ == "__main__":
    try:
        conn = connect_database()
        print(f" Connected to database: {DEFAULT_DB_PATH}")
        close_database(conn)
    except Exception as e:
        print(f" Error: {e}")
