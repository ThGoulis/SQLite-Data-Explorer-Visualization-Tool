import sqlite3

_conn = None  # Global database connection

def set_connection(db_path):
    """Creates a new SQLite connection."""
    global _conn
    if _conn:
        _conn.close()  # Close existing connection
    _conn = sqlite3.connect(db_path)

def get_connection():
    """Returns the SQLite connection."""
    return _conn
