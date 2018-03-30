from flask import Blueprint

auth = Blueprint('authentication', __name__, url_prefix = '/api/v1/auth/')

from application.auth.views import Register,Reset 
from application.users.borrowbook import *

from application import app
from flask_restful import Api

api = Api(app)

api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Reset, '/api/v1/auth/reset')