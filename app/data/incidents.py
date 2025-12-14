import pandas as pd
from pathlib import Path
import sqlite3
from typing import Optional, Union

#Relative imports (works when you run: python3 -m app.data.incidents)
from .db import connect_database
from .schema import create_cyber_incidents_table


DATA_DIR = Path("DATA")  # folder where CSVs live
 
# CRUD FUNCTIONS


def insert_incident(conn: sqlite3.Connection, title, severity, status="open", date=None):
    """Insert a new incident and return its new id."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cyber_incidents (title, severity, status, date)
        VALUES (?, ?, ?, ?)
        """,
        (title, severity, status, date)
    )
    conn.commit()
    return cursor.lastrowid


def get_incident_by_id(conn: sqlite3.Connection, incident_id: int):
    """Fetch one incident by id."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )
    return cursor.fetchone()


def get_all_incidents(conn: sqlite3.Connection):
    """Fetch all incidents."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents")
    return cursor.fetchall()


def update_incident(conn, incident_id, title=None, severity=None, status=None, date=None):
    cursor = conn.cursor()

    # fetch current
    current = get_incident_by_id(conn, incident_id)
    if not current:
        return False

    new_title = title if title is not None else current[1]
    new_severity = severity if severity is not None else current[2]
    new_status = status if status is not None else current[3]
    new_date = date if date is not None else current[4]

    cursor.execute("""
        UPDATE cyber_incidents
        SET title = ?, severity = ?, status = ?, date = ?
        WHERE id = ?
    """, (new_title, new_severity, new_status, new_date, incident_id))

    conn.commit()
    return True


def delete_incident(conn: sqlite3.Connection, incident_id: int):
    """Delete an incident by id."""
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )
    conn.commit()
    return cursor.rowcount


# CSV LOADING


def load_cyber_incidents_csv(conn: sqlite3.Connection, csv_filename="cyber_incidents_1000.csv"):
    """
    Load cyber incidents from CSV into cyber_incidents table.
    CSV columns expected: id,title,severity,status,date
    """
    csv_path = DATA_DIR / csv_filename

    if not csv_path.exists():
        print(f" CSV not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # clean headers

    #  Keep only columns that match your schema
    expected_cols = ["id", "title", "severity", "status", "date"]
    df = df[expected_cols]

    # If you want DB to auto-generate ids, drop id from insert
    df = df.drop(columns=["id"])

    df.to_sql("cyber_incidents", conn, if_exists="append", index=False)

    print(f"Loaded {len(df)} rows into cyber_incidents")
    return len(df)


# --- New helpers: wrappers that open/close DB and ensure table exists ---


def add_incident_db(db_path: Union[str, Path], title: str, severity: str, status: str = "open", date: Optional[str] = None) -> int:
    """
    Open sqlite DB at db_path, ensure cyber_incidents table exists, insert incident and return new id.
    """
    db_path = str(db_path)
    conn = sqlite3.connect(db_path)
    try:
        try:
            create_cyber_incidents_table(conn)
        except Exception:
            # if schema helper not available or fails, proceed and let insert raise if table missing
            pass
        new_id = insert_incident(conn, title, severity, status, date)
        return new_id
    finally:
        conn.close()


def delete_incident_db(db_path: Union[str, Path], incident_id: int) -> int:
    """
    Open sqlite DB at db_path and delete incident by id. Returns number of rows deleted.
    """
    conn = sqlite3.connect(str(db_path))
    try:
        return delete_incident(conn, incident_id)
    finally:
        conn.close()