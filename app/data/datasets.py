import pandas as pd
from pathlib import Path
import sqlite3

from .db import connect_database
from .schema import create_datasets_metadata_table

DATA_DIR = Path("DATA")

# CRUD FUNCTIONS


def insert_dataset(
    conn: sqlite3.Connection,
    dataset_name: str,
    category: str,
    source: str,
    last_updated: str,
    record_count: int,
    file_size_mb: float
):
    """Insert a new dataset row and return its id."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    return cursor.lastrowid


def get_all_datasets(conn: sqlite3.Connection = None):
    """Return all datasets as a DataFrame."""
    close_after = False
    if conn is None:
        conn = connect_database()
        close_after = True

    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )

    if close_after:
        conn.close()

    return df


def delete_dataset(conn: sqlite3.Connection, dataset_id: int):
    """Delete dataset by id. Returns number of deleted rows."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    return cursor.rowcount

# CSV LOADING (2b)

def load_datasets_metadata_csv(
    conn: sqlite3.Connection,
    csv_filename: str = "datasets_metadata_1000.csv"
):
    """
    Load datasets metadata CSV into datasets_metadata table.
    Expected columns: id, dataset_name, category, source, last_updated, record_count, file_size_mb
    """
    create_datasets_metadata_table(conn)

    csv_path = DATA_DIR / csv_filename
    if not csv_path.exists():
        print(f" datasets CSV not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()

    #renaming possible variants
    rename_map = {
        "name": "dataset_name",
        "dataset": "dataset_name",
        "datasetname": "dataset_name",

        "updated": "last_updated",
        "lastupdate": "last_updated",
        "last_updated_date": "last_updated",

        "records": "record_count",
        "recordcount": "record_count",

        "size": "file_size_mb",
        "filesize": "file_size_mb",
        "file_size": "file_size_mb",
    }
    df=df.rename(columns=rename_map)

    expected_cols = ["dataset_name", "category", "source",
        "last_updated", "record_count", "file_size_mb"
    ]

    #keep only cols that exist 
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        print("Your datasets CSV headers are:", list(df.columns))
        print("Still missing columns:", missing)
        return 0
    df = df[expected_cols]

    # Keep ids from CSV (so your counts match the lab)
    df.to_sql("datasets_metadata", conn, if_exists="append", index=False)

    print(f"Loaded {len(df)} rows into datasets_metadata")
    return len(df)