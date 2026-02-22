"""Hotel domain model."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from uuid import uuid4

from .exceptions import EntityNotFoundError, ReservationError, ValidationError
from .storage import JsonStorage


@dataclass
class Hotel:
    """Represents a hotel."""

    id: str
    name: str
    total_rooms: int
    available_rooms: int

    @staticmethod
    def _validate(name: str, total_rooms: int, available_rooms: int) -> None:
        if not name or not name.strip():
            raise ValidationError("Hotel name is required.")
        if not isinstance(total_rooms, int) or total_rooms <= 0:
            raise ValidationError("total_rooms must be a positive integer.")
        if not isinstance(available_rooms, int) or available_rooms < 0:
            raise ValidationError("available_rooms must be non-negative.")
        if available_rooms > total_rooms:
            raise ValidationError("available_rooms cannot exceed total_rooms.")

    @classmethod
    def create(cls, data_dir: Path, name: str, total_rooms: int) -> "Hotel":
        """Create and persist hotel."""
        cls._validate(name, total_rooms, total_rooms)

        storage = JsonStorage(data_dir / "hotels.json")

        hotel = cls(
            id=str(uuid4()),
            name=name.strip(),
            total_rooms=total_rooms,
            available_rooms=total_rooms,
        )

        storage.append(asdict(hotel))
        return hotel

    @classmethod
    def get(cls, data_dir: Path, hotel_id: str) -> "Hotel":
        """Get hotel by id."""
        storage = JsonStorage(data_dir / "hotels.json")
        data = storage.load()

        found = storage.find_by_id(data, hotel_id)

        if not found or not storage.validate_keys(
            found,
            ["id", "name", "total_rooms", "available_rooms"],
        ):
            raise EntityNotFoundError("Hotel not found.")

        return cls(**found)

    @classmethod
    def delete(cls, data_dir: Path, hotel_id: str) -> None:
        """Delete hotel by id."""
        storage = JsonStorage(data_dir / "hotels.json")
        data = storage.load()

        if not storage.find_by_id(data, hotel_id):
            raise EntityNotFoundError("Hotel not found.")

        storage.replace_all(storage.remove_by_id(data, hotel_id))

    @classmethod
    def update(
        cls,
        data_dir: Path,
        hotel_id: str,
        name: str,
        total_rooms: int,
    ) -> "Hotel":
        """Update hotel info."""
        storage = JsonStorage(data_dir / "hotels.json")
        data = storage.load()

        found = storage.find_by_id(data, hotel_id)

        if not found:
            raise EntityNotFoundError("Hotel not found.")

        current_available = int(found.get("available_rooms", 0))

        if current_available > total_rooms:
            raise ValidationError(
                "New total_rooms cannot be less than available_rooms."
            )

        cls._validate(name, total_rooms, current_available)

        found["name"] = name.strip()
        found["total_rooms"] = total_rooms

        storage.replace_all(data)

        return cls(**found)

    @classmethod
    def reserve_room(cls, data_dir: Path, hotel_id: str) -> "Hotel":
        """Decrease available rooms by 1."""
        storage = JsonStorage(data_dir / "hotels.json")
        data = storage.load()

        found = storage.find_by_id(data, hotel_id)

        if not found:
            raise EntityNotFoundError("Hotel not found.")

        if int(found["available_rooms"]) <= 0:
            raise ReservationError("No rooms available.")

        found["available_rooms"] -= 1

        storage.replace_all(data)

        return cls(**found)

    @classmethod
    def cancel_room(cls, data_dir: Path, hotel_id: str) -> "Hotel":
        """Increase available rooms by 1."""
        storage = JsonStorage(data_dir / "hotels.json")
        data = storage.load()

        found = storage.find_by_id(data, hotel_id)

        if not found:
            raise EntityNotFoundError("Hotel not found.")

        if int(found["available_rooms"]) >= int(found["total_rooms"]):
            raise ReservationError("All rooms already available.")

        found["available_rooms"] += 1

        storage.replace_all(data)

        return cls(**found)