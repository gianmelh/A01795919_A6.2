import tempfile
import unittest
from pathlib import Path

from src.exceptions import (
    EntityNotFoundError,
    ReservationError,
    ValidationError,
)
from src.hotel import Hotel


class TestHotel(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_and_get_hotel(self):
        hotel = Hotel.create(self.data_dir, "Hotel Demo", 2)
        fetched = Hotel.get(self.data_dir, hotel.id)
        self.assertEqual(fetched.available_rooms, 2)

    # Negative case 1
    def test_create_hotel_invalid_rooms_raises(self):
        with self.assertRaises(ValidationError):
            Hotel.create(self.data_dir, "Bad Hotel", 0)

    # Negative case 2
    def test_get_missing_hotel_raises(self):
        with self.assertRaises(EntityNotFoundError):
            Hotel.get(self.data_dir, "missing")

    def test_reserve_and_cancel_room(self):
        hotel = Hotel.create(self.data_dir, "Rooms", 1)

        Hotel.reserve_room(self.data_dir, hotel.id)
        fetched = Hotel.get(self.data_dir, hotel.id)
        self.assertEqual(fetched.available_rooms, 0)

        Hotel.cancel_room(self.data_dir, hotel.id)
        fetched2 = Hotel.get(self.data_dir, hotel.id)
        self.assertEqual(fetched2.available_rooms, 1)

    # Negative case 3
    def test_reserve_no_rooms_raises(self):
        hotel = Hotel.create(self.data_dir, "Full", 1)
        Hotel.reserve_room(self.data_dir, hotel.id)

        with self.assertRaises(ReservationError):
            Hotel.reserve_room(self.data_dir, hotel.id)

    # Negative case 4
    def test_cancel_when_all_available_raises(self):
        hotel = Hotel.create(self.data_dir, "Empty", 1)
        with self.assertRaises(ReservationError):
            Hotel.cancel_room(self.data_dir, hotel.id)
