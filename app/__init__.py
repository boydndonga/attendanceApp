from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()



def create_app(config_state):

    app = Flask(__name__)
    app.config.from_object(config[config_state])

    db.init_app(app)
    ma.init_app(app)

    from .attendanceV1 import apiV1
    app.register_blueprint(apiV1, url_prefix = '/api/v1')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')

    return app
