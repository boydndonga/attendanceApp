from . import auth
from .. import db
from ..models import User, user_schema
from flask import request, jsonify, make_response


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        pass_secure = data.get('password')
        user = User(username=username, email=email, password=pass_secure)
        if user.validate_email() is True:
            if user.validate_password(pass_secure) is True:
                if user.verify_email() is False:
                    user.gravatar()
                    db.session.add(user)
                    db.session.commit()
                    return make_response(jsonify({'message': 'successfully created user'}), 201)
                return make_response(jsonify({'message': 'user in existence'}), 406)
            return make_response(jsonify({'message': 'password at least 8 characters of numbers/letters/special char'})
                                 , 403)
        return make_response(jsonify({'message': 'invalid email'}), 403)
    return make_response(jsonify({'message':'invalid request'}), 404)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        pass_secure = data.get('password')
        user = User(username=username, email=email, password=pass_secure)
        query_user = User.query.filter_by(email=email).first()
        try:
            verified_user = user.verify_email()
            print(verified_user)
            if verified_user:
                verified_pass = query_user.verify_password(pass_secure)
                if verified_pass:
                    access_token = query_user.generate_confirmation_token()
                    if access_token:
                        return make_response(jsonify({'message': 'login successful', 'access_token':access_token}), 200)
                raise Exception('password is incorrect')
            raise Exception('user does not exist, register first')
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 403)
    return make_response(jsonify({'message': 'invalid request'}), 404)