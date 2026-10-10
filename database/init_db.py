import os
import sqlite3
from contextlib import closing
from typing import Optional


def initialize_database(db_path: Optional[str] = None) -> str:
    """Create the local flight search tables and return the database path."""
    if db_path is None:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flights.db")
    with closing(sqlite3.connect(db_path)) as connection, connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS flight_searches (
                search_id TEXT PRIMARY KEY,
                departure TEXT NOT NULL,
                arrival TEXT NOT NULL,
                outbound_date TEXT NOT NULL,
                return_date TEXT,
                trip_type TEXT NOT NULL,
                adults INTEGER NOT NULL,
                children INTEGER NOT NULL DEFAULT 0,
                min_price REAL,
                max_price REAL,
                flight_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS flight_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id TEXT NOT NULL,
                flight_data TEXT NOT NULL,
                FOREIGN KEY (search_id) REFERENCES flight_searches(search_id)
                    ON DELETE CASCADE
            );
            """
        )
    return db_path


if __name__ == "__main__":
    print(f"Initialized flight database at {initialize_database()}")
