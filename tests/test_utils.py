import os
import tempfile
import unittest
from datetime import date
from unittest.mock import patch

from utils import (
    get_api_key,
    get_search_file,
    parse_iso_date,
    validate_date_range,
)


class UtilityTests(unittest.TestCase):
    def test_api_key_requires_configured_value(self):
        with patch.dict(os.environ, {"SERPAPI_KEY": "   "}):
            with self.assertRaisesRegex(ValueError, "not configured"):
                get_api_key()

    def test_api_key_returns_configured_value(self):
        with patch.dict(os.environ, {"SERPAPI_KEY": "test-key"}):
            self.assertEqual(get_api_key(), "test-key")

    def test_search_file_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Invalid search ID"):
                get_search_file(directory, "..\\outside")

    def test_date_validation_and_range(self):
        self.assertEqual(parse_iso_date("2030-01-02", "date"), date(2030, 1, 2))
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            parse_iso_date("2030-1-2", "date")
        with self.assertRaisesRegex(ValueError, "must be after"):
            validate_date_range(date(2030, 1, 3), date(2030, 1, 2), "start", "end")


if __name__ == "__main__":
    unittest.main()
