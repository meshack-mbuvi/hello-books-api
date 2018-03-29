
# Blueprint names
from application.books import book
from application.users import user
from application.auth import auth

from application import app

# Register the blueprints
app.register_blueprint(book)
app.register_blueprint(user)
app.register_blueprint(auth)


if __name__ == '__main__':
	app.run(debug = True)