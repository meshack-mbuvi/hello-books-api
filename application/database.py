from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask import Flask 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello_books.sqlite3'

db = SQLAlchemy(app)

# models here 
class Book(db.Model):
	__tablename__ = "books"
	book_id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(64),index=True, unique=True)
	available = db.Column(db.Boolean, default=True)


class Ubsers(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	password = db.Column(db.String)

	
class BookRentals(db.Model):
	__tablename__ = "bookrentals"
	id = db.Column(db.Integer, primary_key=True)
	borrowed_date = db.Column(db.DateTime)
	return_date = db.Column(db.DateTime)

	# relationships
	username = db.Column(db.Integer,db.ForeignKey("users.username"), unique=False, nullable=False)
	book_id = db.Column(db.Integer,db.ForeignKey("books.book_id"), unique=False)

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)