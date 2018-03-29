from flask import Blueprint

# This blueprint is registered in the run module

book = Blueprint('books', __name__, url_prefix='/api/v1/books/')

from application.books.views import books
from application.books import models

from application import app
from flask_restful import Api

api = Api(app)

api.add_resource(books, '/api/v1/books/', '/api/v1/books/<id>/')


