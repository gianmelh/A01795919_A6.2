import tempfile
import unittest
from pathlib import Path

from src.storage import JsonStorage


class TestStorageInvalidJson(unittest.TestCase):
    def test_load_invalid_json_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "bad.json"
            file_path.write_text("{not valid json]", encoding="utf-8")

            storage = JsonStorage(file_path)
            data = storage.load()

            self.assertEqual(data, [])

    def test_load_non_list_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "weird.json"
            file_path.write_text('{"a": 1}', encoding="utf-8")

            storage = JsonStorage(file_path)
            data = storage.load()

            self.assertEqual(data, [])