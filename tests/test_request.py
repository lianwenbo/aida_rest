
import requests
token_url = 'http://localhost:5000/aida/auth2/token'
get_user_url = 'http://localhost:5000/aida/user/%d'
verify_code_url = 'http://localhost:5000/aida/get_verify_code'
headers = {}

user_1 = {'phone': 'xxxxx', 'password': 'user_1'}

user_2 = {'phone': 'xxxx', 'password': 'user_2'}


def post_token(u_info):
    res = requests.post(token_url, data=u_info)
    return res.json()


def get_user(user_id, token):
    headers['Authorization'] = 'Bearer %s' % token
    res = requests.get(get_user_url % user_id, headers=headers)
    return res.text


def verify_code(phone_num):
    args = {'phone': phone_num}
    res = requests.get(verify_code_url, args)
    if res.status_code == 400:
        return res.text
    elif res.status_code == 200:
        return res.json()['verify_code']
    else:
        return 'Unknow error'

#code = verify_code(user_1['phone'])
#print('the code is:', code)
#user_1['verification_code'] = code
#tok_res = post_token(user_1)
#print('the token res is:', tok_res)
#user_res = get_user(tok_res['user_id'], tok_res['access_token'])
#print('the user_res is:', user_res)

