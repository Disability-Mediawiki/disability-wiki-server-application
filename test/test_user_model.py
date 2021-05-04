import unittest

# from app import db
from app.main.model import User
from test.base import BaseTestCase, db


class TestUserModel(BaseTestCase):

    def test_create_db(self):
        db.create_all()

    def test_encode_auth_token(self):

        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))


if __name__ == '__main__':
    test_create_db()
    unittest.main()
