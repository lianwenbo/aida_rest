from . import db, bcrypt, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import time


class User(db.Model):
    """User model for storing User related details"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(128))
    point = db.Column(db.Integer, default=0)
    avatar = db.Column(db.String(1024), default='')
    phone = db.Column(db.String(16), unique=True, index=True)
    verified = db.Column(db.Boolean, default=False)
    verify_code = db.Column(db.String(6))
    launch_timestamp = db.Column(db.Float)

    def __init__(self, phone, verify_code):
        self.phone = phone
        self.verify_code = verify_code
        self.launch_timestamp = time.time()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_token(self):
        app.logger.debug('the secret in generate %s', app.config['SECRET_KEY'])
        serializer = Serializer(app.config['SECRET_KEY'],
                                expires_in=app.config['TOKEN_EXPIRED'])
        return serializer.dumps({'user_id': self.id})

