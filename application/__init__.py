
from flask import Flask
app = Flask(__name__)

app.secret_key = 'secret'

users_table = {}
books_in_api = {}
books_record = {}
