from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from instance.config import configuration


app = Flask(__name__, static_folder=None)
api = Api(app)


def app_config(config):
    app.config.from_object(configuration[config])


jwt = JWTManager(app)
db = SQLAlchemy(app)

from .views.user_account import Register, Reset, Login, Logout
from .views.borrowbook import Borrow
from .views.manage_book import Books

user = Blueprint('users', __name__, url_prefix='/api/v1/users/')
book = Blueprint('books', __name__, url_prefix='/api/v1/books/')
auth = Blueprint('authentication', __name__, url_prefix='/api/v1/auth/')

api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Reset, '/api/v1/auth/reset')
api.add_resource(Login, '/api/v1/auth/login')
api.add_resource(Logout, '/api/v1/auth/logout')
api.add_resource(Borrow, '/api/v1/users/books/<isbn>')
api.add_resource(Books, '/api/v1/books/', '/api/v1/books/<isbn>')


