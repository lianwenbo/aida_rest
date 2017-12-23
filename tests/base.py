from flask_testing import TestCase
from app import db, app


class BaseTestCase(TestCase):
    """ Base Tests"""

    def setup(self):
        db.create_all()
        db.session.commit()

    def teradown(self):
        db.session.remove()
        db.drop_all()
