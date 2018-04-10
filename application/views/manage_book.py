from application.models.bookmodels import Book
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import *

# prepare project seeds
book = Book('Mbuvi', 'Python  programming')
books_in_api[len(books_in_api) + 1] = book
book = Book('Mbuvi', 'C++  programming')
books_in_api[len(books_in_api) + 1] = book
book = Book('Mbuvi', 'Flask  programming')
books_in_api[len(books_in_api) + 1] = book
book = Book('Mbuvi', 'Android  programming')
books_in_api[len(books_in_api) + 1] = book
book = Book('Mbuvi', 'PHP  programming')
books_in_api[len(books_in_api) + 1] = book


class Books(Resource):
    """This resource is used to manage books in the library
    """

    def correct(self, data):
        result = [c for c in data if c.isdigit()]
        if len(result) == 0 and len(data) > 0:
            return True
        return False

    def isadmin(self, username):
        users = [user for user in users_table.values() if user.username == username and user.admin]
        if len(users) > 0:
            return True
        else:
            return False

    def get(self, book_id=None):
        """ This method returns a book or all books depending whether id is set or not."""
        if book_id is not None:
            try:
                book_id = int(book_id)
                book_data = dict()
                book_data[book_id] = books_in_api[book_id].__dict__
                return book_data, 200
            except KeyError:
                return 'Book not found', 404

        else:
            # show all books
            books = {}
            for key in books_in_api:
                books[key] = books_in_api[key].__dict__

            return books, 200

    @jwt_required
    def post(self):
        """create new book
        Book title and author must be provided in order to create a new book
        """
        current_user = get_jwt_identity()
        if not self.isadmin(current_user):
            return {'message': 'Only an administrator can add new book'}, 401

        data = request.get_json()
        if 'title' in data and 'author' in data:
            title = data['title']
            author = data['author']
            if not self.correct(title) or not self.correct(author):
                return {'message': 'Author and title can only be non-empty strings '}, 400

            book_data = [book for book in books_in_api.values() if book.title == title]
            if book_data:
                return {'message': 'Book already exists in the system'}, 301
            new_book = Book(title, author)
            books_in_api[len(books_in_api) + 1] = new_book

            return new_book.__dict__, 201

        return {'message': 'Book "author" and "title" must be provided'}, 400

    @jwt_required
    def delete(self, book_id):
        """This method deletes a book item from the app
        Only an administrator can delete a book"""
        current_user = get_jwt_identity()
        if self.isadmin(current_user):
            try:
                # cannot delete an already borrowed book
                if not books_in_api[int(book_id)].available:
                    return {"Message": "Book already borrowed."}, 304
                del books_in_api[int(book_id)]
                # Return the remaining books after deletion
                return self.get(),
            except KeyError:
                return {'message': 'Book with that id does not exist'}, 404
        else:
            return {'message': 'Only an administrator can delete a book'}, 401

    @jwt_required
    def put(self, book_id):
        # confirm we have the right format and required fields
        current_user = get_jwt_identity()
        if self.isadmin(current_user):
            data = request.get_json()
            if not data or 'author' not in data or 'title' not in data:
                return {'message': 'Ensure to use json format and fill all fields'}, 400

            title = data['title']
            author = data['author']
            if self.correct(title) and self.correct(author):
                book_id = int(book_id)
                try:
                    # make sure to convert to integer
                    books_in_api[book_id].title = title
                    books_in_api[book_id].author = author
                    return {'message': 'book updated'}, 200

                except Exception as e:
                    print(e)
                    # Book not found in the database
                    return {'message': 'book with that id not found'}, 404
            else:
                return {'message': 'Only strings can be used in data fields.'}, 400

        else:
            return {'message': 'Only an administrator can modify book data'}, 401
