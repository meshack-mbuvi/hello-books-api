from application.books.models import Book
from flask_restful import Resource
from flask import request

# Holds all books in the app
books_in_api = []

class books(Resource):

    def get(self, id=None):
        if id != None:
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
        if len(items) == 0:
            return 1
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

        return (data), 201
    def delete(self, id):
        # find the item to delete
        books = [book for book in books_in_api if book.id == id]

        if len(books) < 1:
            # book not found
            return 'Item not found', 404

        # delete the item from the list
        books_in_api.remove(books[0])

        return self.get()

    def make_response(self, Book):
        data = {'id': Book.id, 'title': Book.title, 'author': Book.author}

        return data

    def put(self):
        # confirm we have the right format and required fields
        if not request.json or 'author' not in request.json or 'title' not in request.json:
            abort(400)
        item_id = request.json['id']
        title = request.json['title']
        author = request.json['author']

        items = [book for book in books_in_api if book.id == item_id]

        # Drop the item from the list
        books_in_api.remove(items[0])

        items[0].id = item_id

        items[0].title = title
        items[0].author = author

        # Add the item with new data to the list
        books_in_api.append(items[0])
           
        return ({'id':items[0].id,'title':items[0].title,'author':items[0].author}),200


