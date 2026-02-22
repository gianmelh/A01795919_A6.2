import tempfile
import unittest
from pathlib import Path

from src.customer import Customer
from src.exceptions import (
    EntityNotFoundError,
    ReservationError,
    ValidationError,
)
from src.hotel import Hotel
from src.reservation import Reservation


class TestReservation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.tmp.name)
        self.customer = Customer.create(self.data_dir, "Lin", "lin@demo.com")
        self.hotel = Hotel.create(self.data_dir, "Hotel", 1)

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_and_cancel_reservation(self):
        reservation = Reservation.create(
            self.data_dir,
            self.customer.id,
            self.hotel.id,
        )
        self.assertEqual(reservation.status, "ACTIVE")

        canceled = Reservation.cancel(self.data_dir, reservation.id)
        self.assertEqual(canceled.status, "CANCELED")

        hotel = Hotel.get(self.data_dir, self.hotel.id)
        self.assertEqual(hotel.available_rooms, 1)

    # Negative case 1
    def test_create_reservation_missing_customer_id_raises(self):
        with self.assertRaises(ValidationError):
            Reservation.create(self.data_dir, "", self.hotel.id)

    # Negative case 2
    def test_create_reservation_customer_not_found_raises(self):
        with self.assertRaises(EntityNotFoundError):
            Reservation.create(
                self.data_dir,
                "missing",
                self.hotel.id,
            )

    # Negative case 3
    def test_cancel_twice_raises(self):
        reservation = Reservation.create(
            self.data_dir,
            self.customer.id,
            self.hotel.id,
        )
        Reservation.cancel(self.data_dir, reservation.id)

        with self.assertRaises(ReservationError):
            Reservation.cancel(self.data_dir, reservation.id)
