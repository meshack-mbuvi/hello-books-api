from flask import Blueprint

user = Blueprint('users', __name__, url_prefix = '/api/v1/users/')

from application.users.views import Users, Borrow
from application.users import models

from application import app
from flask_restful import Api

api = Api(app)

api.add_resource(Users, '/api/v1/users/')
api.add_resource(Borrow, '/api/v1/users/books/')