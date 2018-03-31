
from flask import Flask
app = Flask(__name__)


users_table = {}
books_in_api = {}
books_record = {}

# Blueprint names
from application.books import book
from application.users import user
from application.auth import auth
from application.docs.views import docs

# Register the blueprints
app.register_blueprint(book)
app.register_blueprint(user)
app.register_blueprint(auth)
app.register_blueprint(docs)
