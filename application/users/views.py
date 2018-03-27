from flask_restful import Resource
from flask import request, jsonify

from application.books.views import books_in_api

# get list of users in the app
from application.auth.views import users_table


class Users(Resource):

    def get(self, username=None):
        # TODO: Return all the books the user has borrowed

        return {'message': 'Welcome here. You can borrow books now'}, 200


class Borrow(Resource):

    def post(self):
        # This method is used for borrowing a new book
        # Let us load the book with the id given
        item_id = request.json['id']
        book = [item for item in books_in_api ]
        print(book[0].id)

        # Confirm there is a book to rent
        if not book:
            return {"Message": "No book found with the given book id"}, 404
        # Set the book to be unavailable
        book[0].available = False

        # Get the username for user who send the request
        username = request.json['username']

        # Get the user object from existing users matching the given username
        user = [user for user in users_table if user.username == username]

        # Check that we found the user
        if not user:
        	return {"Message":"No user with the username provided"}, 404

        # Add the book object to the user's list of borrowed borrowings
        user[0].borrowed_books.append(book)

        return ({'User': user[0].username, "borrowings": user[0].borrowed_books}), 201
