import sqlite3


def create_users_table(conn: sqlite3.Connection):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        );
    """)
    conn.commit()
    print("users table created successfully!")


def create_cyber_incidents_table(conn: sqlite3.Connection):
    """Create cyber_incidents table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            date TEXT NOT NULL
        );
    """)
    conn.commit()
    print("cyber_incidents table created successfully!")


def create_datasets_metadata_table(conn: sqlite3.Connection):
    """Create datasets_metadata table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source TEXT NOT NULL,
            category TEXT NOT NULL,
            size INTEGER NOT NULL
        );
    """)
    conn.commit()
    print("datasets_metadata table created successfully!")


def create_it_tickets_table(conn: sqlite3.Connection):
    """Create it_tickets table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_date TEXT NOT NULL
        );
    """)
    conn.commit()
    print("it_tickets table created successfully!")


def create_all_tables(conn: sqlite3.Connection):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("all tables created successfully!")