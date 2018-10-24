from flask import Blueprint

apiV1 = Blueprint('api', __name__)

from . import views, validation