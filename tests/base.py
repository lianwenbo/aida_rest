from flask_testing import TestCase
from app import db, create_app


class BaseTestCase(TestCase):
    """ Base Tests"""

    def create_app(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        return self.app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

