from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__, static_folder=None)
from flask_restful import Api

api = Api(app)

from instance.config import configuration
app.config.from_object(configuration['staging'])
jwt = JWTManager(app)

# To be used for storing blacklisted tokens
blacklist = set()

users_table = {}
books_in_api = {}