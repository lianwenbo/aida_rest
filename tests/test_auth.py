from tests.base import BaseTestCase


class TestAuthView(BaseTestCase):
    def test_verifycode(self):
        with self.client:
            phone_num = '7965321'
            response = self.client.get('/aida/get_verify_code?phone=%s' % phone_num)
            print('the response result %s' % str(response.json))
            self.assertEqual(response.json['phone'], phone_num)
            self.assertEqual(response.status_code, 200)

