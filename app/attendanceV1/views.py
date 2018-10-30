from . import apiV1
from app.models import users_schema, User
from flask_login import login_required
from flask import request, jsonify, make_response

# endpoint to show all users
@apiV1.route("/users", methods=["GET"])
def get_user():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            if auth_header.split(" ")[1]:
                pass
            raise Exception('Authorization is empty')
        raise Exception('no Authorization available')
    except Exception as e:
        return make_response(jsonify({'message':str(e)}), 401)
    # auth_header = request.headers.get('Authorization')
    # access_token = auth_header.split(" ")[1]
    # all_users = User.query.all()
    # result = users_schema.dump(all_users)
    # return jsonify(result.data)
