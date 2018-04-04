
from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
app = Flask(__name__)

from instance.config import configuration
app.config.from_object(configuration['testing'])
jwt = JWTManager(app)

# To be used for storing blacklisted tokens
blacklist = set()

users_table = {}
books_in_api = {}
