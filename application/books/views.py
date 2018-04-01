from application.books.models import Book
from flask_restful import Resource
from flask import request

from application import books_in_api


class Books(Resource):

    def get(self, id=None):
        if id != None:
            # find the specific item
            book = books_in_api[int(id)]

            if not book:
                # book not found
                return 'Book not found', 404
            return (book), 200

        else:

            if len(books_in_api) < 1:
                # book not found
                return 'Books not found', 404
            return books_in_api, 200

    def generateID(self, data):
        # If no data alredy in the dictionary, return 1
        if len(data) == 0:
            return 1

        # add 1 to the size of the dictionary object
        return str(len(data) + 1)

    def post(self):
        # confirm we have the right format and required fields are field
        if not request.json or 'author' not in request.json or 'title' not in request.json:
            return {'message': 'Ensure you use the correct format and all fields are filled'}, 400

        
        title = request.json['title']
        author = request.json['author']

        # check fields are not empty
        if not author or not title:
            return {'message':'book title and author cannot be empty'},400

        # Get next id for the book
        book_id = self.generateID(books_in_api)

        # find if there is a book with that information
        for key in books_in_api:
            if books_in_api[key]['title'] == title and books_in_api[key]['author'] == author:
                return {'message': 'Book already exists in the system'}, 301

        # create new book object
        book = Book(title, author)
        book_details = book.getdetails()

        # add new book object now
        books_in_api[book_id] = book_details

        return (book_details), 201

    def delete(self, id):

        # confirm there is a book in our dictionary
        if len(books_in_api) < 1:
            # book not found
            return 'Item not found', 404

        # delete the item from the dictionary
        del books_in_api[int(id)]

        # Return the remaining books after deletion
        return self.get(), 200

    def make_response(self, Book):
        data = {'id': Book.id, 'title': Book.title, 'author': Book.author}

        return data

    def put(self):
        # confirm we have the right format and required fields
        if not request.json or 'author' not in request.json or 'title' not in request.json:
            abort(400)

        # Retrieve data sent by client
        book_id = request.json['id']
        title = request.json['title']
        author = request.json['author']

        # Edit the book info
        books_in_api[book_id]['title'] = title
        books_in_api[book_id]['author'] = author

        return books_in_api[book_id], 200
