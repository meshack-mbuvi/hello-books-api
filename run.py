# Blueprint names
from application import book
from application import user
from application import auth

from application import app


# from application import users_table, books_in_api
# from application.users.usermode import User
# from application.books.models import Book
from application.docs.views import docs

# Register the blueprints
app.register_blueprint(book)
app.register_blueprint(user)
app.register_blueprint(auth)
app.register_blueprint(docs)

if __name__ == '__main__':
	app.run(debug=True)
