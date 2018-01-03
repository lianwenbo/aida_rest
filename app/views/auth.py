# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify, make_response, g
from flask.views import MethodView
from flask_httpauth import HTTPTokenAuth
from flask import current_app as app
from random import randint
from .. import db
from ..models import User
from itsdangerous import SignatureExpired, BadSignature, \
    TimedJSONWebSignatureSerializer as Serializer
import time
import uuid

auth = HTTPTokenAuth()
auth_blueprint = Blueprint('auth', __name__)

business_id = uuid.uuid4()


@auth.verify_token
def verify_token(token):
    g.user_id = None
    try:
        app.logger.debug('the secret key %s', app.config['SECRET_KEY'])
        serializer = Serializer(app.config['SECRET_KEY'],
                                expires_in=app.config['TOKEN_EXPIRED'])
        app.logger.debug('token is %s with expired in %d',
                         token, app.config['TOKEN_EXPIRED'])
        data = serializer.loads(token)
    except SignatureExpired:
        app.logger.warning('Signature Expired for token %s', token)
        g.status = -1
        return False
    except BadSignature:
        app.logger.warning('Bad Signature for token %s', token)
        g.status = -2
        return False
    user = User.query.filter_by(id=data['user_id']).first()
    if not user:
        g.status = -3
        return False
    g.user_id = data['user_id']
    return True


def generate_rand_digits(n):
    digits = ''
    for i in range(n):
        digits += str(randint(0, 9))
    return digits


class GetVerifyCode(MethodView):
    """
    get verify code from client to phone
    """
    def get(self):
        phone = request.args['phone']
        user = User.query.filter_by(phone=phone).first()
        digits = generate_rand_digits(6)
        if not user:
            u = User(phone=phone, verify_code=digits)
            db.session.add(u)
        elif time.time() - user.launch_timestamp > app.config['GET_CODE_PERIOD']:
            user.launch_timestamp = time.time()
            user.verify_code = digits
            db.session.add(user)
        else:
            msg = '<h1>user resubmit to frequent please resubmit after %d ' \
                  'seconds</h1>' % app.config.get('GET_CODE_PERIOD', 60)
            return make_response(jsonify({'message': msg}), 400)
        if 'PRODUCT_MODE' in app.config and app.config['PRODUCT_MODE']:
            from send_sms import send_sms, SIGN_NAME, TEMPLATE_CODE
            params = {'code': digits, 'product': 'aida'}
            send_state = send_sms(business_id, phone, SIGN_NAME,
                                  TEMPLATE_CODE, params)
            app.logger.debug('the send state %s', send_state)
        db.session.commit()
        if app.config.get('TESTING'):
            return make_response(jsonify({'phone': phone, 'verify_code': digits})), 200
        else:
            return make_response(jsonify({}), 200)


class UserGetAPI(MethodView):
    """
    User Registeration Resource
    """
    decorators = [auth.login_required]

    def get(self, user_id):
        user = User.query.filter_by(id=g.user_id).first()
        app.logger.debug('before user get with user id %s', g.user_id)
        if user:
            res = {'id': user.id, 'name': user.name,
                   'point': user.point, 'avatar': user.avatar,
                   'phone': user.phone}
            return make_response(jsonify(res)), 200
        return '<h1>the user id %s not found!</h1>' % user_id, 400


class GetAndSetToken(MethodView):
    """
    User get or set the token
    """
    def post(self):
        phone = request.values['phone']
        password = request.values['password']
        user = User.query.filter_by(phone=phone).first()
        if not user:
            msg = '<h1>The user not exists</h1>'
            return make_response(jsonify({'message': msg}), 401)
        if 'verify_code' in request.values:
            verified_code = request.values['verify_code']
            if verified_code != user.verify_code:
                msg = '<h1>verify code not right resubmit</h1>'
                return make_response(jsonify({'message': msg}), 402)
            else:
                user.password = password
                user.verified = True
                res = dict()
                res['user_id'] = user.id
                res['phone'] = user.phone
                token = user.generate_token()
                res['access_token'] = token.decode('utf-8')
                res['user_name'] = user.name
                res['expires_in'] = app.config['TOKEN_EXPIRED']
                return make_response(jsonify(res)), 200
        else:
            if not user.verified:
                msg = 'Not verify please input the verification_code'
                return make_response(jsonify({'message': msg}), 403)
            if user.check_password(password):
                res = dict()
                res['user_id'] = user.id
                res['phone'] = user.phone
                res['access_token'] = str(user.generate_token())
                res['user_name'] = user.name
                res['expires_in'] = app.config['TOKEN_EXPIRED']
                return make_response(jsonify(res)), 200
            else:
                return make_response('password not right', 405)


user_get_view = UserGetAPI.as_view('user_get_api')
get_verify_code = GetVerifyCode.as_view('get_verify_code')
get_and_set_token = GetAndSetToken.as_view('get_and_set_token')


auth_blueprint.add_url_rule('/aida/user/<user_id>', view_func=user_get_view,
                            methods=['GET'])
auth_blueprint.add_url_rule('/aida/get_verify_code',
                            view_func=get_verify_code, methods=['GET'])
auth_blueprint.add_url_rule('/aida/auth2/token', view_func=get_and_set_token,
                            methods=['POST'])
