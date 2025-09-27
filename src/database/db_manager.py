import sqlite3
from sqlite3 import Error
from typing import Optional, List, Tuple, Any


def close_connection(conn: Optional[sqlite3.Connection]):
    """Close the provided database connection."""
    if conn:
        conn.close()


class DatabaseManager:
    def __init__(self, db_file: str):
        """Initialize the DatabaseManager with a database file."""
        self.db_file = db_file

    def create_connection(self) -> Optional[sqlite3.Connection]:
        """Create a database connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(f"Error creating connection: {e}")
            return None

    def execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> sqlite3.Cursor:
        """Execute a single query and return the cursor."""
        conn = self.create_connection()
        if conn is None:
            raise ConnectionError("Failed to create a database connection.")

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor  # Return the cursor for further operations
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            conn.rollback()
            raise
        finally:
            close_connection(conn)

    def fetch_query(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple]:
        """Fetch results from a query."""
        conn = self.create_connection()
        results = []

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
        except Error as e:
            print(f"Error fetching query results: {e}")
        finally:
            close_connection(conn)

        return results

    @staticmethod
    def get_last_insert_id(cursor: sqlite3.Cursor) -> int:
        """Get the last inserted ID using the provided cursor."""
        return cursor.lastrowid
