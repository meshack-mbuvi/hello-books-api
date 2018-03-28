from application.books.models import Book
from flask_restful import Resource


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
                items.append({'id': book.id, 'title': book.title, 'author': book.author})
            return (items), 200


