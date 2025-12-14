import pandas as pd
from .db import connect_database  # Assuming .db contains connect_database
import sqlite3

# FIX 1 & 2: Defines the missing function, using correct table name 'it_tickets'
def get_all_tickets(conn: sqlite3.Connection):
    """
    Retrieves all IT tickets from the database.
    
    :param conn: The database connection object.
    :return: A list of dictionaries, where each dictionary represents a ticket.
    """
    cursor = conn.cursor()
    
    # Corrected table name to 'it_tickets' and selected columns match schema
    query = "SELECT id, title, priority, status, created_date FROM it_tickets"
    
    try:
        cursor.execute(query)
        # Get column names to use as dictionary keys
        columns = [col[0] for col in cursor.description]
        
        # Fetch all results and combine with column names
        tickets = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return tickets
    except Exception as e:
        print(f"Error fetching all tickets: {e}") 
        return []

# FIX 3: Defines the missing bulk loading function
def load_it_tickets_csv(conn: sqlite3.Connection, file_path="DATA/it_tickets.csv"):
    """
    Loads IT tickets data from a CSV file into the 'it_tickets' table.
    
    :param conn: The database connection object.
    :param file_path: Path to the IT tickets CSV file.
    :return: The number of rows loaded.
    """
    try:
        # 1. Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        
        # 2. Use the pandas to_sql method to write data to the SQLite table
        # if_exists='append' adds new rows, index=False skips writing the DataFrame index
        df.to_sql('it_tickets', conn, if_exists='append', index=False)
        
        return len(df)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {file_path}")
        return 0
    except Exception as e:
        print(f"Error loading IT tickets CSV: {e}")
        return 0


def update_ticket_priority(ticket_id: int, new_priority: str):
    """
    Updates the priority of an IT ticket. 
    Note: This function uses connect_database() internally, which may be inconsistent
    with other functions that take `conn` as an argument.
    """
    conn = connect_database() 
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE it_tickets SET priority = ? WHERE id = ?""",
        (new_priority, ticket_id))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0