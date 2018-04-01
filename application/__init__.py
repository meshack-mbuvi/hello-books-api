
from flask import Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

users_table = {}
books_in_api = {}
books_record = {}
