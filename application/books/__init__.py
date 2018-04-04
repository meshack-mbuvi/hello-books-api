from flask import Blueprint

# This blueprint is registered in the run module

book = Blueprint('books', __name__, url_prefix='/api/v1/books/')

from application.books.views import Books
from application.books import models

from application import api

api.add_resource(Books, '/api/v1/books/', '/api/v1/books/<id>')


