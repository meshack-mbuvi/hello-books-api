from application.books.models import Book
from flask_restful import Resource
from flask import request


books_in_api = []

bk = Book(1, 'Test Driven Development', 'Kent Beck')
books_in_api.append(bk)
bk1 = Book(4, 'Test Driven Development', 'Kent Beck')

books_in_api.append(bk1)


class books(Resource):

    def get(self, id=''):
        if id != '':
            # items to return
            items = []
            # find the specific item
            items = [book for book in books_in_api if book.id == id]
            if len(items) < 1:
                # book not found
                return 'Item not found', 404
            return ({'Book': {'id': items[0].id, 'title': items[0].title, 'author': items[0].author}}), 200

        else:
            # items to return
            items = []
            if len(books_in_api) < 1:
                # book not found
                return 'Books not found', 404
            for book in books_in_api:
                items.append(
                    {'id': book.id, 'title': book.title, 'author': book.author})
            return (items), 200

    def generateID(self):
        # Get the ids already assigned and sort them in ascending order
        items = [book.id for book in books_in_api]
        items.sort()
        newID = items[-1] + 1
        return newID

    def make_response(self, Book):
        data = {'id': Book.id, 'title': Book.title, 'author': Book.author}

        return data

    def post(self):
        # confirm we have the right format and required fields
        if not request.json or 'author' not in request.json or 'title' not in request.json:
            abort(400)

        # Get next id for the book
        book_id = self.generateID()
        title = request.json['title']
        author = request.json['author']

        # create new book object
        book = Book(book_id, title, author)

        # add new book object now
        books_in_api.append(book)

        # format data to be returned to the calling client
        data = self.make_response(book)

        return (data), 200
