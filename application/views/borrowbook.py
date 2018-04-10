from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from . import books_in_api, users_table


class Borrow(Resource):

    @jwt_required
    def post(self, book_id):
        try:
            # Let us load the book with the id given
            book = books_in_api[int(book_id)]
            if not book.available:
                return {"Message": "Book is not available for renting"}

            # Get the username of user who send the request
            current_user = get_jwt_identity()
            user_object = {}
            for key in users_table:
                if users_table[key].username == current_user:
                    # save key to user_object dictionary; key is the user_id
                    user_object['user_id'] = key

            book.available = False
            book.user_id = user_object['user_id']
            return book.__dict__, 200
        except KeyError:
            return {'Message': 'Book with that Id is not available'}, 404
