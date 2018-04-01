import unittest

from flask_restful import Resource
from flask import request, jsonify


from application.books.views import books_in_api
from application.users.bookrentals import BookRentals

# get list of users in the app
from application import users_table, books_record


class Borrow(Resource):

    def post(self):
        # Let us load the book with the id given
        book_id = request.json['id']

        # Confirm there is a book to rent
        try:
            book = books_in_api[book_id]
        except:
            return {'Message': 'Book with that Id isnot available'}, 404

        # Set the book to be unavailable
        book['available'] = False

        # Get the username of user who send the request
        username = request.json['username']

        # confirm user has an account with us
        for key in users_table:
            if users_table[key]['username'] == username:
                # create a new row with details of the username and bookid,etc
                rentals = BookRentals(
                    username, book_id, 'to be set', 'to be set')

                # save the borrowing record to our table.
                books_record[len(books_record) + 1] = rentals.getdetails()

                # Notify the user
                books = rentals.getdetails()
                books['book_id'] = book_id
                return books, 201

            else:
                return {"Message": "No user with the username provided"}, 404
