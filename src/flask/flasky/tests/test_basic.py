import unittest
from flask import  current_app
from app import create_app, db


class BasicTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_flask_app_exist(self):
        self.assertFalse(current_app is None)

    def test_flask_app_test_context(self):
        self.assertTrue(current_app.config["TESTING"])


if __name__ == "__main__":
    unittest.main()
