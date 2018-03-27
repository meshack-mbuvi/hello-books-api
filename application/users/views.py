from flask_restful import Resource
from flask import request,jsonify

from application.books.views import books_in_api

# get list of users in the app
from application.auth.views import users_table

class Users(Resource):

	def get(self, username=None):
		# TODO: Return all the books the user has borrowed



		return {'message':'Welcome here. You can borrow books now'},200

class Borrow(Resource):
	def post(self):
		# This method is used for borrowing a new book
		# Let us load the book with the id given
		item_id = request.json['id']
		book = [item for item in books_in_api if item.id == item_id]
		book[0].available = False

		username = request.json['username']

		user = [user for user in users_table if user.username == username]

		user[0].borrowed_books.append(book)

		return ({'User':user[0].username,"borrowings":user[0].borrowed_books}),201