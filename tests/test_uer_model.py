from base import BaseTestCase
from app.models import User
from app import db
from app.views.auth import verify_token
from flask import g
import time


class TestUserModel(BaseTestCase):
    def test_token_generate(self):
        user = User('phone_number', '123456')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.id, 1)
        self.assertEqual(self.app.config['TOKEN_EXPIRED'], 3)
        token = user.generate_token()
        self.assertTrue(verify_token(token))
        self.assertEqual(g.user_id, 1)
        time.sleep(4)
        self.assertFalse(verify_token(token))
