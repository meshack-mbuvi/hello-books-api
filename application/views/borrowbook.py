from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from application.models.bookmodels import *
from application.models.usermodel import *


class Borrow(Resource):

    @jwt_required
    def post(self, isbn):
        """This method handles requests for borrowing books
        It retrieves the book from the database using the isbn provided, checks whether the book is already
        borrowed(available is False for borrowed book),assigns the book to the user and sets it to be unavailable
        for borrowing.
        :arg
            isbn (str)- the isbn for a particular book
        :return message and status code for success or failure.

        """
        book = db.session.query(Book).filter(Book.isbn == isbn).first()
        if book is not None:
            if not book.available:
                return {"Message": "Book is not available for renting"}, 423

            # Retrieve user_id of the user who sent the request
            current_user = get_jwt_identity()
            user = db.session.query(User).filter(User.username == current_user).first()
            user.books.append(book)
            book.available = False
            db.session.commit()

            return {'message': 'You have borrowed book with isbn{}'.format(isbn)}, 200

        else:
            return {'Message': 'Book with that isbn is not available'}, 404
