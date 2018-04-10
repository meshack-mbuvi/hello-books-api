from application.models.bookmodels import Book
from flask_restful import Resource
from flask import request

from . import books_in_api

# prepare project seeds
book = Book('Mbuvi','Python  programming')
books_in_api.append(book)
book = Book('Mbuvi','C++  programming')
books_in_api.append(book)
book = Book('Mbuvi','Flask  programming')
books_in_api.append(book)
book = Book('Mbuvi','Android  programming')
books_in_api.append(book)
book = Book('Mbuvi','PHP  programming')
books_in_api.append(book)


class Books(Resource):
    """This resource is used to manage books in the library

    """

    def correct(self, data):
        for char in data:
            if not char.isdigit():
                return True
            return False

    def get(self, id=None):
        # This method returns a book or all books depending whether id is set or not.
        if id != None:
            try:
                book_id = int(id)
                book = books_in_api[book_id]
                book['id'] = book_id
                return (book), 200
            except Exception as e:
                # book not found
                return 'Book not found', 404

        else:
            # Returning all books
            return books_in_api, 200


    def post(self):
        '''create new book
        '''
        title = request.json['title']
        author = request.json['author']
        if request.json and author and title:            

            # find if there is a book with that information
            for key in books_in_api:
                if books_in_api[key]['title'] == title and books_in_api[key]['author'] == author:
                    return {'message': 'Book already exists in the system'}, 301

                # create new book object
                book = Book(title, author)
                book_details = book.__dict__
                # add new book object now
                books_in_api[len(books_in_api) + 1] = book_details

                return (book_details), 201
            

        return {'message': 'use json and make sure book title and author are not empty'}, 400
       

    def delete(self, id):

        # the book id may not exist in our system
        try:
            del books_in_api[int(id)]
            # Return the remaining books after deletion
            return self.get(), 200
        except Exception as e:
            return {'message': 'Book with that id does not exist'}, 404

    def put(self):
        # confirm we have the right format and required fields
        data = request.get_json()
        if not data or not data['author'] or not data['title']:
            return {'message': 'Ensure to use json format and fill all fields'}, 400

        # Retrieve data sent by client
        book_id = data['id']
        title = data['title']
        author = data['author']
        if self.correct(title) and self.correct(author):
            # The book may not be exisiting
            try:
                # make sure to convert to integer
                bk_id = int(book_id)
                books_in_api[bk_id]['title'] = title
                books_in_api[bk_id]['author'] = author
                return {'message': 'book updated'}, 200

            except Exception as e:
                # Book not found in the database
                return {'message': 'book with that id not found'}, 404

        return {'message': 'Do not use numbers in your fields'}, 400