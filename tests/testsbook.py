import unittest
import json

# common module sets path for the parent module

from run import app
from application.books.models import Book
from application.books.views import books_in_api


class BookAPITests(unittest.TestCase):

    def setUp(self):
        # Prepare for testing;set up variables
        self.app = app
        # create books(instances of Books class) for testing.
        self.bk = Book('Test Driven Development', 'Kent Beck')
        books_in_api[1] = self.bk.getdetails()

        self.bk1 = Book('Python Programming', 'Peter Carl')

        books_in_api[3] = self.bk1.getdetails()

        self.app = self.app.test_client()
        self.BASE_URL = 'http://localhost:5000/api/v1/books/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None

    def test_get_all_books(self):
        ''' test the api can retrieve books
        '''
        resp = self.app.get(self.BASE_URL)
        self.assertEqual(resp.status_code, 200,
                         msg='Should retrieve data from the api.')

        data = json.loads(resp.get_data().decode('utf-8'))

        # Test title for book with id==3
        test_book_title = 'Python Programming'

        # test_item should be in the list
        self.assertEqual(test_book_title, data['3'][
                         'title'], msg='Should retrieve items')

    def test_get_a_single_book(self):
        ''' test the api can retrieve books
        '''
        book_id = 3
        resp = self.app.get(self.BASE_URL + '%d/' % book_id)

        self.assertEqual(resp.status_code, 200,
                         msg='Should retrieve data from the api.')

        data = json.loads(resp.get_data().decode('utf-8'))

        test_book = {'title': 'Python Programming', 'author': 'Peter Carl'}

        # test_item should be in the list
        self.assertTrue(test_book == {'author': books_in_api[3]['author'], 'title': books_in_api[3]['title']},
                        msg='Should retrieve an item with id = item_id')

    def test_post_book(self):
        '''This method tests that the api can save data.'''
        # book to post
        book = {'title': 'Test Driven Developemnt',
                'author': 'Kent Beck'}

        resp = self.app.post(self.BASE_URL, data=json.dumps(
            book), content_type='application/json')

        self.assertEqual(resp.status_code, 201,
                         msg='Should create data')

        # confirm that data has been saved
        data = json.loads(resp.get_data().decode('utf-8'))
        test_data = {'title': data['title'], 'author': data['author']}

        self.assertEqual(book, test_data,
                         msg='The api should save data for new book item')

    def test_post_existing_book_fails(self):
        '''This method tests that the api can save data.'''
        # book to post
        book = {'title': 'Test Driven Developemnt',
                'author': 'Kent Beck'}

        initial_no_of_books = len(books_in_api)

        resp = self.app.post(self.BASE_URL, data=json.dumps(
            book), content_type='application/json')

        self.assertEqual(resp.status_code, 301,
                         msg='Should create data')

        # get new size after adding new book
        new_no_of_books = len(books_in_api)

        self.assertEqual(initial_no_of_books, new_no_of_books,
                         msg='Should not create a book if it exists')

    def test_post_book_with_empty_fields_fails(self):
        '''This method tests that the api can save data.'''
        # book to post
        book = {'title': '',
                'author': ''}

        initial_no_of_books = len(books_in_api)

        resp = self.app.post(self.BASE_URL, data=json.dumps(
            book), content_type='application/json')

        self.assertEqual(resp.status_code, 400,
                         msg='Bad format')

        # get new size after adding new book
        new_no_of_books = len(books_in_api)

        self.assertEqual(initial_no_of_books, new_no_of_books,
                         msg='Should not create a book if fields are empty')

    def test_post_book_using_bad_format_fails(self):
        '''This method tests that the api can save data.'''
        # book to post
        book = {'title': ''}

        initial_no_of_books = len(books_in_api)

        resp = self.app.post(self.BASE_URL, data=json.dumps(
            book), content_type='application/json')

        self.assertEqual(resp.status_code, 400,
                         msg='Bad format')

        # get new size after adding new book
        new_no_of_books = len(books_in_api)

        self.assertEqual(initial_no_of_books, new_no_of_books,
                         msg='Should not create a book if some fields are missing')

    def test_delete_item(self):
        ''' test the api can delete a book
        '''

        item_id = 1
        resp = self.app.delete(self.BASE_URL + '%d/' % item_id)
        if resp.status_code == 404:
            return
        self.assertEqual(resp.status_code, 200,
                         msg='The api should be reachable')

        test_book = ('Test Driven Development', 'Kent Beck')

        # Lets confirm the book does not exist
        try:
            data = books_in_api[1]
        except:
            return True

    def test_edit_book(self):
        '''This endpoint updates information for a given book'''

        book_id = 1
        new_info = {'id': book_id, 'title': 'Learn Java the Hard way',
                    'author': 'Meshack'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_info), content_type='application/json')

        self.assertEqual(resp.status_code, 200,
                         msg="Endpoint should be reachable")

        data = json.loads(resp.get_data().decode('utf-8'))

        res = data['author']

        self.assertEqual(
            res, 'Meshack', msg='Should update the information for specified book')


if __name__ == '__main__':
    unittest.main(verbosity=2)
