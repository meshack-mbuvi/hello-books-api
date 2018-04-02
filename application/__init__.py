
from flask import Flask
app = Flask(__name__)

from instance.config import configuration

users_table = {}
books_in_api = {}
books_record = {}
