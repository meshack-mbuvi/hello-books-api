from flask import Blueprint

user = Blueprint('users', __name__, url_prefix='/api/v1/users/')

from application.users.borrowbook import  Borrow

from application import api

api.add_resource(Borrow, '/api/v1/users/books/<book_id>')

