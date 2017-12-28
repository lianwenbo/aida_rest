from flask_testing import TestCase
from app import set_app_config, app


class TestBaseConfigCase(TestCase):
    def create_app(self):
        self.app = app
        set_app_config(self.get_config_name())
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.config = self.app.config
        return app

    def get_config_name(self):
        raise NotImplementedError('not impl')

    def tearDown(self):
        self.app_context.pop()


class TestDevelopmentConfig(TestBaseConfigCase):
    def get_config_name(self):
        return 'development'

    def test_debug_mode(self):
        self.assertTrue(self.config['DEBUG'])

    def test_expired_elapsed(self):
        self.assertEqual(self.config['TOKEN_EXPIRED'], 1800)
        self.assertEqual(self.config['VERIFY_EXPIRED'], 300)

    def test_access_key_not_auth(self):
        self.assertEqual(self.config['ACCESS_KEY_ID'], 'not authorize')
        self.assertEqual(self.config['ACCESS_KEY_SECRET'], 'secret not auth')
        self.assertEqual(len(self.config['SECRET_KEY']), 24)

    def test_sql_track_modifications(self):
        self.assertFalse(self.config['SQLALCHEMY_TRACK_MODIFICATIONS'])


class TestTestingConfig(TestBaseConfigCase):
    def get_config_name(self):
        return 'testing'

    def test_testing(self):
        self.assertTrue(self.config['TESTING'])

    def test_token_expired(self):
        self.assertEqual(self.config['TOKEN_EXPIRED'], 3)
        self.assertEqual(self.config['VERIFY_EXPIRED'], 3)


class TestProductionConfig(TestBaseConfigCase):
    def get_config_name(self):
        return 'production'

    def test_production_mode(self):
        self.assertTrue(self.config['PRODUCT_MODE'])
