"""Reservation domain model."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from uuid import uuid4

from .customer import Customer
from .exceptions import EntityNotFoundError, ReservationError, ValidationError
from .hotel import Hotel
from .storage import JsonStorage


@dataclass
class Reservation:
    """Represents a reservation."""

    id: str
    customer_id: str
    hotel_id: str
    status: str  # ACTIVE or CANCELED

    @staticmethod
    def _validate(customer_id: str, hotel_id: str) -> None:
        if not customer_id:
            raise ValidationError("customer_id is required.")
        if not hotel_id:
            raise ValidationError("hotel_id is required.")

    @classmethod
    def create(cls, data_dir: Path, customer_id: str, hotel_id: str) -> "Reservation":
        """Create a reservation and reserve a room."""
        cls._validate(customer_id, hotel_id)

        # Validate entities exist
        _ = Customer.get(data_dir, customer_id)
        _ = Hotel.get(data_dir, hotel_id)

        # Reserve a room (may fail)
        Hotel.reserve_room(data_dir, hotel_id)

        storage = JsonStorage(data_dir / "reservations.json")

        reservation = cls(
            id=str(uuid4()),
            customer_id=customer_id,
            hotel_id=hotel_id,
            status="ACTIVE",
        )

        storage.append(asdict(reservation))
        return reservation

    @classmethod
    def get(cls, data_dir: Path, reservation_id: str) -> "Reservation":
        """Get reservation by id."""
        storage = JsonStorage(data_dir / "reservations.json")
        data = storage.load()

        found = storage.find_by_id(data, reservation_id)

        if not found or not storage.validate_keys(
            found, ["id", "customer_id", "hotel_id", "status"]
        ):
            raise EntityNotFoundError("Reservation not found.")

        return cls(**found)

    @classmethod
    def cancel(cls, data_dir: Path, reservation_id: str) -> "Reservation":
        """Cancel reservation and release one room."""
        storage = JsonStorage(data_dir / "reservations.json")
        data = storage.load()

        found = storage.find_by_id(data, reservation_id)

        if not found:
            raise EntityNotFoundError("Reservation not found.")

        if found.get("status") != "ACTIVE":
            raise ReservationError("Reservation is not active.")

        found["status"] = "CANCELED"
        storage.replace_all(data)

        Hotel.cancel_room(data_dir, found["hotel_id"])

        return cls(**found)