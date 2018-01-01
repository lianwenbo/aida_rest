from tests.base import BaseTestCase
import time
from flask import current_app as app
import json


class TestAuthView(BaseTestCase):
    def test_verifycode(self):
        with self.client:
            phone_num = '7965321'
            response = self.client.get('/aida/get_verify_code?phone=%s' % phone_num)
            self.assertEqual(response.json['phone'], phone_num)
            self.assertEqual(response.status_code, 200)
            rep_resp = self.client.get('/aida/get_verify_code?phone=%s' % phone_num)
            self.assertEqual(rep_resp.status_code, 400)
            time.sleep(app.config.get('GET_CODE_PERIOD', 60))
            rep_resp = self.client.get('/aida/get_verify_code?phone=%s' % phone_num)
            self.assertEqual(rep_resp.status_code, 200)

    def test_get_and_set_token(self):
        with self.client:
            post_dict = {'phone': '7965321', 'password': '123456'}
            resp = self.client.post('/aida/auth2/token', data=post_dict)
            self.assertEqual(resp.status_code, 401)
            get_code_resp = self.client.get('/aida/get_verify_code?phone=%s' %
                                            post_dict['phone'])
            self.assertEqual(get_code_resp.status_code, 200)
            resp = self.client.post('/aida/auth2/token', data=post_dict)
            self.assertEqual(resp.status_code, 403)
            post_dict['verify_code'] = '1'
            resp = self.client.post('/aida/auth2/token', data=post_dict)
            self.assertEqual(resp.status_code, 402)
            post_dict['verify_code'] = get_code_resp.json['verify_code']
            resp = self.client.post('/aida/auth2/token', data=post_dict)
            self.assertEqual(resp.status_code, 200)
            post_dict['password'] = '1'
            resp = self.client.post('/aida/auth2/token', data=post_dict)
            self.assertEqual(resp.status_code, 405)





