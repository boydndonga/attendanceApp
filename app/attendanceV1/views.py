from . import apiV1
from flask import jsonify
from app.models import users_schema


# endpoint to show all users
@apiV1.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)