from application.books import book

from application import app


# Register the blueprints
app.register_blueprint(book)

if __name__ == '__main__':
	app.run(debug = True)