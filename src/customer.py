"""Customer domain model."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from uuid import uuid4

from .exceptions import EntityNotFoundError, ValidationError
from .storage import JsonStorage


@dataclass
class Customer:
    """Represents a customer."""

    id: str
    full_name: str
    email: str

    @staticmethod
    def _validate(full_name: str, email: str) -> None:
        if not full_name or not full_name.strip():
            raise ValidationError("Customer full_name is required.")
        if not email or "@" not in email:
            raise ValidationError("Customer email is invalid.")

    @classmethod
    def create(cls, data_dir: Path, full_name: str, email: str) -> "Customer":
        """Create and persist a customer."""
        cls._validate(full_name, email)

        storage = JsonStorage(data_dir / "customers.json")

        customer = cls(
            id=str(uuid4()),
            full_name=full_name.strip(),
            email=email.strip(),
        )

        storage.append(asdict(customer))
        return customer

    @classmethod
    def get(cls, data_dir: Path, customer_id: str) -> "Customer":
        """Get customer by id."""
        storage = JsonStorage(data_dir / "customers.json")
        data = storage.load()

        found = storage.find_by_id(data, customer_id)

        if not found or not storage.validate_keys(
            found, ["id", "full_name", "email"]
        ):
            raise EntityNotFoundError("Customer not found.")

        return cls(**found)

    @classmethod
    def delete(cls, data_dir: Path, customer_id: str) -> None:
        """Delete customer by id."""
        storage = JsonStorage(data_dir / "customers.json")
        data = storage.load()

        if not storage.find_by_id(data, customer_id):
            raise EntityNotFoundError("Customer not found.")

        storage.replace_all(storage.remove_by_id(data, customer_id))

    @classmethod
    def update(
        cls,
        data_dir: Path,
        customer_id: str,
        full_name: str,
        email: str,
    ) -> "Customer":
        """Update existing customer."""
        cls._validate(full_name, email)

        storage = JsonStorage(data_dir / "customers.json")
        data = storage.load()

        found = storage.find_by_id(data, customer_id)

        if not found:
            raise EntityNotFoundError("Customer not found.")

        found["full_name"] = full_name.strip()
        found["email"] = email.strip()

        storage.replace_all(data)

        return cls(**found)
