"""JSON file storage with error handling."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List


class JsonStorage:
    """Simple JSON storage class for lists of dictionaries."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.save([])

    def load(self) -> List[dict]:
        """Load data from JSON file.

        If file is invalid, print error and return empty list.
        """
        try:
            content = self.file_path.read_text(encoding="utf-8").strip()
            if not content:
                return []

            data = json.loads(content)

            if not isinstance(data, list):
                print(f"[ERROR] Invalid format in {self.file_path}")
                return []

            return data

        except (json.JSONDecodeError, OSError) as error:
            print(f"[ERROR] Could not read {self.file_path}: {error}")
            return []

    def save(self, data: List[dict]) -> None:
        """Save list of dictionaries to JSON file."""
        self.file_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def append(self, item: dict) -> None:
        """Append one item to file."""
        data = self.load()
        data.append(item)
        self.save(data)

    def replace_all(self, data: List[dict]) -> None:
        """Replace file content."""
        self.save(data)

    @staticmethod
    def find_by_id(data: List[dict], entity_id: str) -> dict | None:
        """Find dictionary by id."""
        for item in data:
            if item.get("id") == entity_id:
                return item
        return None

    @staticmethod
    def remove_by_id(data: List[dict], entity_id: str) -> List[dict]:
        """Remove dictionary by id."""
        return [item for item in data if item.get("id") != entity_id]

    @staticmethod
    def validate_keys(obj: Any, required_keys: List[str]) -> bool:
        """Validate required keys in dictionary."""
        return isinstance(obj, dict) and all(
            key in obj for key in required_keys
        )
