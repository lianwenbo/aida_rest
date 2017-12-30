from flask_testing import TestCase
from app import app, db


class BaseTestCase(TestCase):
    """ Base Tests"""

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        self.app = app
        self.app_context = app.app_context()
        self.app_context.push()
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

