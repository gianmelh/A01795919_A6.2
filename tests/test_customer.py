import tempfile
import unittest
from pathlib import Path

from src.customer import Customer
from src.exceptions import EntityNotFoundError, ValidationError


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_and_get_customer(self):
        customer = Customer.create(
            self.data_dir,
            "Ada Lovelace",
            "ada@demo.com",
        )
        fetched = Customer.get(self.data_dir, customer.id)
        self.assertEqual(fetched.email, "ada@demo.com")

    # Negative case 1
    def test_create_customer_invalid_email_raises(self):
        with self.assertRaises(ValidationError):
            Customer.create(self.data_dir, "Bad Email", "not-an-email")

    # Negative case 2
    def test_create_customer_empty_name_raises(self):
        with self.assertRaises(ValidationError):
            Customer.create(self.data_dir, "", "a@b.com")

    # Negative case 3
    def test_get_nonexistent_customer_raises(self):
        with self.assertRaises(EntityNotFoundError):
            Customer.get(self.data_dir, "missing-id")

    # Negative case 4
    def test_delete_nonexistent_customer_raises(self):
        with self.assertRaises(EntityNotFoundError):
            Customer.delete(self.data_dir, "missing-id")

    def test_update_customer(self):
        customer = Customer.create(self.data_dir, "Grace Hopper", "g@demo.com")
        updated = Customer.update(
            self.data_dir, customer.id, "Grace M. Hopper", "grace@demo.com"
        )
        self.assertEqual(updated.full_name, "Grace M. Hopper")
        self.assertEqual(updated.email, "grace@demo.com")
