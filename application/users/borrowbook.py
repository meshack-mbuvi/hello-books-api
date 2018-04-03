import unittest

from flask_restful import Resource
from flask import request, jsonify


from application import books_in_api
from application.users.bookrentals import BookRentals

# get list of users in the app
from application import users_table


class Borrow(Resource):

    def post(self, book_id):
        
        try:
            # Let us load the book with the id given
            
            book = books_in_api[int(book_id)] 

            # Get the username of user who send the request
            username = request.json['username']

            # confirm user has an account with us
            for key in users_table:
                if users_table[key]['username'] == username:
                    # Set the book to be unavailable
                    book['available'] = False
                    book['user_id'] = users_table[key]['id']
                    return books, 200

                else:
                    return {"Message": "No user with the username provided"}, 404
        except:
            return {'Message': 'Book with that Id is not available'}, 404
