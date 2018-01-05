from tests.base import BaseTestCase
import time
from flask import current_app as app
import json


class TestAuthView(BaseTestCase):
    def test_verifycode(self):
        with self.client:
            phone_num = '7965321'
            response = self.client.get('/aida/verification_code?phone=%s' % phone_num)
            self.assertEqual(response.json['phone'], phone_num)
            self.assertEqual(response.status_code, 200)
            post_dict = {'phone': phone_num,
                         'verification_code': response.json['verification_code']}
            auth_response = self.client.post('/aida/auth2/verification_code', data=post_dict)
            self.assertEqual(auth_response.status_code, 200)
            self.assertEqual(auth_response.json['user_name'], '')
            register_dict = {'password': '123456', 'user_name': 'llll'}
            headers = dict(Authorization='Bearer ' + auth_response.json['access_token'])
            register_response = self.client.post('/aida/auth2/registeration',
                                                 data=register_dict, headers=headers)
            print(register_response)
            self.assertEqual(register_response.status_code, 200)

