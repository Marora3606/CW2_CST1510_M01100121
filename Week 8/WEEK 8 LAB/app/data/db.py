"""Database Connection Module"""

import sqlite3
from pathlib import Path

# Default database path: resolve relative to the project (two levels up from this file)
# so running the script from a different working directory still finds the DATA folder
DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "DATA" / "intelligence_platform.db"


def connect_database(db_path: Path = DEFAULT_DB_PATH):
    """Connect to SQLite database. Creates parent directories if needed.

    db_path may be a Path or string. The function ensures the parent directory
    exists before calling sqlite3.connect so SQLite can create the DB file.
    """
    # Allow strings to be passed in
    db_path = Path(db_path)

    # Ensure parent directory exists so sqlite can create the database file
    parent = db_path.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        # If we cannot create the directory, raise a clearer error
        raise sqlite3.OperationalError(f"Unable to create database directory: {parent}")

    return sqlite3.connect(str(db_path))



def close_database(conn):
    """Close the database connection safely."""
    if conn:
        conn.close()


if __name__ == "__main__":
    try:
        conn = connect_database()
        # DEFAULT_DB_PATH is the canonical path used by connect_database
        print(f" Connected to database: {DEFAULT_DB_PATH}")
        close_database(conn)
    except Exception as e:
        print(f" Error: {e}")
