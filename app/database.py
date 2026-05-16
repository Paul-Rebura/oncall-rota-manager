import sqlite3

DB_NAME = "oncall_rota.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialise_db():
    """Create all tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS engineers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rota (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            engineer_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            shift TEXT NOT NULL CHECK(shift IN ('day', 'night')),
            FOREIGN KEY (engineer_id) REFERENCES engineers(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rota_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            severity TEXT NOT NULL CHECK(severity IN ('low', 'medium', 'high', 'critical')),
            description TEXT,
            raised_at TEXT NOT NULL,
            resolved INTEGER DEFAULT 0,
            FOREIGN KEY (rota_id) REFERENCES rota(id)
        )
    """)

    conn.commit()
    conn.close()

