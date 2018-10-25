from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from . import ma, db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50),unique = True, index= True)
    users = db.relationship('User', backref='role', lazy = True)

    def __repr__(self):
        return f'User {self.name}'
