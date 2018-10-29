import hashlib
import re
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from . import ma, db
from flask import current_app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255),unique = True,index = True, nullable=False)
    pass_secure = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    avatar_hash = db.Column(db.String(255))
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'User {self.username}'

    def validate_email(self):
        if len(self.email) != 0:
            if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)", self.email):
                return True
            return False

    def validate_password(self,password):
        if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            return True
        return False

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.pass_secure != u2.pass_secure)

    def verify_email(self):
        mail = User.query.filter_by(email=self.email).first()
        if mail:
            return True
        return False

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def gravatar_hash(self):
        hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.gravatar_hash()
        self.avatar_hash =  '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
        return self.avatar_hash


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email', 'avatar_hash')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50),unique = True, index= True)
    users = db.relationship('User', backref='role', lazy = True)

    def __repr__(self):
        return f'User {self.id}'
