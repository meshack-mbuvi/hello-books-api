from application.books import books

from flask import Flask 

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(books)

if __name__ == '__main__':
	app.run(debug = True)