import os
import sqlite3
import tempfile
import unittest
from contextlib import closing

from database.init_db import initialize_database


class DatabaseTests(unittest.TestCase):
    def test_initialize_database_creates_schema_at_requested_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "flights.db")
            self.assertEqual(initialize_database(path), path)
            with closing(sqlite3.connect(path)) as connection:
                tables = {
                    row[0]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }
        self.assertTrue({"flight_searches", "flight_results"}.issubset(tables))


if __name__ == "__main__":
    unittest.main()
