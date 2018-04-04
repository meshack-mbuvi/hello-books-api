from flask import Blueprint

auth = Blueprint('authentication', __name__, url_prefix = '/api/v1/auth/')

from application.auth.views import Register,Reset, Login ,Logout
from application.users.borrowbook import *

from application import api

api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Reset, '/api/v1/auth/reset')
api.add_resource(Login, '/api/v1/auth/login')
api.add_resource(Logout, '/api/v1/auth/logout')