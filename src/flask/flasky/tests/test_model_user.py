import unittest
from flask import current_app
from app.models import User


class BasicTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_password_hash_generated(self):
        u = User(password="ok")
        self.assertTrue(u.password_hash is not None)

    def test_password_not_readable(self):
        u = User(password="ok")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verify_works_correctly(self):
        u = User(password="ok")
        self.assertTrue(u.password_verify("ok"))
        self.assertFalse(u.password_verify("o"))

    def test_password_unique_hashes_for_the_same_password(self):
        u1 = User(password="ok")
        u2 = User(password="ok")
        self.assertNotEquals(u1.password_hash, u2.password_hash)


if __name__ == "__main__":
    unittest.main()
