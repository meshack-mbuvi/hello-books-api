from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from application.models.bookmodels import *
from application.models.usermodel import *


class Books(Resource):
    """This class is used to manage books in the library
    Processes like book creation, edit, deletion and retrieval are done in this class.

    """

    def correct(self, data):
        """checks whether specified data is a valid string.
        :arg
            param1 (str) data: parameter to be checked.
        :returns True for string data only, False otherwise.

        """
        result = [c for c in data if c.isdigit()]
        if len(result) == 0 and len(data) > 0:
            return True
        return False

    def isadmin(self, username):
        """checks whether user with provided username is an admin.
        :arg
            username (str): parameter to be considered.
        :returns
            True for admin, False for non-admin.

        """
        user = db.session.query(User).filter(User.username == username).first()
        if user.admin:
            return True
        else:
            return False

    def get(self, isbn=None):
        """ Retrieves a book or all books depending whether id is set or not.
        We query book,author and book_category to get all book details and then prepare a dictionary object with the
        book data which is returned to the user client
        :arg
            isbn (str):
        :returns
            dictionary with a book or books.

        """
        if isbn is not None:
            book_data = dict()
            book = db.session.query(Book.isbn, Book.available, BookCategory.title, Author.author_data) \
                .join(BookCategory, (BookCategory.cat_id == Book.cat_id)) \
                .join(Author, (Author.author_id == Book.author_id)).filter(Book.isbn == isbn).first()
            if book is not None:
                book_data['isbn'] = book.isbn
                book_data['title'] = book.title
                book_data['author'] = book.author_data
                book_data['available'] = book.available
                return book_data, 200
            return 'Book not found', 404

        else:
            # show all books
            all_books = {}
            books = db.session.query(Book.isbn, Book.available, BookCategory.title, Author.author_data) \
                .join(BookCategory, (BookCategory.cat_id == Book.cat_id)) \
                .join(Author, (Author.author_id == Book.author_id)).filter(Book.available == True).all()
            if books is not None:
                for book in books:
                    book_data = dict()
                    book_data['isbn'] = book.isbn
                    book_data['title'] = book.title
                    book_data['author'] = book.author_data
                    book_data['available'] = book.available
                    all_books[book.isbn] = book_data
                return all_books, 200
            else:
                return 'No book found', 404

    @jwt_required
    def post(self):
        """creates new book
        Book isbn, title and author must be provided in order to create a new book
        :return
            dictionary object with message and status code of the request.

        """
        current_user = get_jwt_identity()
        if not self.isadmin(current_user):
            return {'message': 'Only an administrator can add new book'}, 401

        data = request.get_json()
        if 'title' in data and 'author' in data:
            title = data['title']
            author_details = data['author']
            isbn = data['isbn']
            if not self.correct(title) or not self.correct(author_details):
                return {'message': 'Author and title can only be non-empty strings '}, 400

            # check whether book exists in the database
            book = db.session.query(Book).filter(Book.isbn == isbn).first()

            if book is not None:
                return {'message': 'Book already exists in the system'}, 409

            new_book = Book(isbn)
            new_book.save()
            # create book category if it does not exist and add book to the category specified
            category = db.session.query(BookCategory).filter(BookCategory.title == title).first()
            if category is None:
                category = BookCategory(title)
                category.save()
            category.books.append(new_book)
            category.copies += 1

            # check whether author specified exists
            author = db.session.query(Author).filter(Author.author_data == author_details).first()
            if author is None:
                author = Author(author_details)
                author.save()
            author.books.append(new_book)
            author.books_authored += 1
            db.session.commit()

            return {'message': 'Book added to system'}, 201

        return {'message': 'Book "author" and "title" must be provided'}, 400

    @jwt_required
    def delete(self, isbn):
        """This method deletes a book item from the app
        Only an administrator can delete a book
        :arg
            isbn (str)
        :returns
            dictionary with remaining books or message and status code depending on request results.

        """
        current_user = get_jwt_identity()
        if self.isadmin(current_user):
            book = db.session.query(Book).filter(Book.isbn == isbn).first()
            if book is not None:
                # check whether book is already borrowed
                if not book.available:
                    return {"Message": "Book already borrowed."}, 304
                else:
                    db.session.delete(book)
                    # Return the remaining books after deletion
                    return self.get()
            else:
                return {'message': 'Book with that id does not exist'}, 404
        else:
            return {'message': 'Only an administrator can delete a book'}, 401

    @jwt_required
    def put(self, isbn):
        """Handles updates to book data.
        Basically, after confirming for required privileges, query database for book with specified isbn, if author
        information is to be changed, decrease the number of books authored by current author and delete author if
        s/he has zero books.Update details for new author as required. Do the same for book title which
        gives bookcategory.
        :arg
            isbn (str)
        :returns
            message or dictionary with book info and status code.

        """
        current_user = get_jwt_identity()
        if self.isadmin(current_user):
            data = request.get_json()
            if not data or 'author' not in data or 'title' not in data:
                return {'message': 'Ensure to use json format and fill all fields'}, 400

            title = data['title']
            author_details = data['author']
            if self.correct(title) and self.correct(author_details):
                book = db.session.query(Book).filter(Book.isbn == isbn).first()
                if book is not None:
                    # if we are changing author information for the book
                    author = db.session.query(Author).filter(Author.author_id == book.author_id).first()
                    if author.author_data != author_details:
                        # remove book from author's list and reduce the number of books authored by this author
                        author.books.remove(book)
                        author.books_authored -= 1
                        db.session.commit()
                        # create new author if author does not exist and add the book to his/her list of books authored
                        author = db.session.query(Author).filter(Author.author_data == author_details).first()
                        if author is None:
                            author = Author(author_details)
                        author.books.append(book)
                        author.books_authored += 1
                        author.save()

                    # Get and see if we are changing book title(category)
                    category = db.session.query(BookCategory).filter(BookCategory.cat_id == book.cat_id).first()
                    if category.title != title:
                        # remove book from existing category
                        category.books.remove(book)
                        category.copies -= 1
                        db.session.commit()
                        # create new category if category does not exist and add book to it.
                        category = db.session.query(BookCategory).filter(BookCategory.title == title).first()
                        if category is None:
                            category = BookCategory(title)
                        category.books.append(book)
                        category.copies += 1
                        category.save()

                    # assemble data to return to user client
                    book_data = dict()
                    book_data['title'] = category.title
                    book_data['author'] = author.author_data

                    return book_data, 200
                else:
                    return {'message': 'book with that isbn is not found'}, 404
            else:
                return {'message': 'Only strings can be used in data fields.'}, 400

        else:
            return {'message': 'Only an administrator can modify book data'}, 401
