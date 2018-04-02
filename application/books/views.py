from application.books.models import Book
from flask_restful import Resource
from flask import request

from application import books_in_api


class Books(Resource):

    def correct(self, data):
        for char in data:
            if not char.isdigit():
                return True
            return False

    def get(self, id=None):
        if id != None:
            # find the specific item
            try:
                book_id = int(id)
                book = books_in_api[book_id]
                return (book), 200
            except Exception as e:
                # book not found
                return 'Book not found', 404

        else:
            # Returning all books
            return books_in_api, 200


    def post(self):
        # confirm we have the right format and required fields are field
        if not request.json or 'author' not in request.json or 'title' not in request.json:
            return {'message': 'Ensure you use the correct format and all fields are filled'}, 400

        

        # check fields are not empty
        if author and title:
            title = request.json['title']
            author = request.json['author']

            # find if there is a book with that information
            for key in books_in_api:
                if books_in_api[key]['title'] == title and books_in_api[key]['author'] == author:
                    return {'message': 'Book already exists in the system'}, 301

                # create new book object
                book = Book(title, author)
                book_details = book.getdetails()
                # add new book object now
                books_in_api[len(books_in_api) + 1] = book_details

                return (book_details), 201
            

        return {'message': 'book title and author cannot be empty'}, 400
       

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
