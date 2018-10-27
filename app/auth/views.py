from . import auth
from .. import db
from ..models import User
from flask import request, jsonify, make_response


# @auth.route('/register', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return 'posted'
#     return make_response(jsonify({'message':'make post request'}))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'posted'
    return make_response(jsonify({'message':'make post request'}))