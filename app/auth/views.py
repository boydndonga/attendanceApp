from . import auth
from .. import db
from ..models import User,user_schema
from flask import request, jsonify, make_response


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        pass_secure = data.get('password')
        user = User(username=username, email=email, pass_secure=pass_secure)
        if user.validate_email() is True:
            if user.validate_password() is True:
                user.gravatar()
                db.session.add(user)
                db.session.commit()
                return make_response(jsonify({'message': 'successfully created user'}), 201)
            return make_response(jsonify({'message': 'password at least 8 characters of numbers/letters/special char'})
                                 , 403)
        return make_response(jsonify({'message': 'invalid email'}), 403)
    return make_response(jsonify({'message':'invalid request'}), 404)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'posted'
    return make_response(jsonify({'message':'make post request'}))