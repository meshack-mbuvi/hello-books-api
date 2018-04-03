from run import *
import unittest
import json
from instance.config import configuration


class TestsBook(unittest.TestCase):

    def setUp(self):
            # create new user
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()
        

        # Prepare for testing;set up variables
        self.user = User(username="mbuvi", password="mesh")
        users_table[len(users_table) + 1] = self.user.getdetails()

        self.users_table = users_table

        # add a book to the app
        book = Book('Marcos', 'Learn Android the Hard way')
        books_in_api[len(books_in_api)] = book.getdetails()

        self.BASE_URL = 'http://localhost:5000/api/v1/books/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        self.users_table = None

    def test_edit_book(self):
        '''This endpoint updates information for a given book'''
        new_info = {'id': 0, 'title': 'Learn Java the Hard way',
                    'author': 'Meshack'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_info), content_type='application/json')
        self.assertEqual(resp.status_code, 200,
                         msg="Endpoint should be reachable")

        data = json.loads(resp.get_data().decode('utf-8'))

        msg = data['message']

        self.assertEqual(msg, 'book updated',
                         msg='Should update the information for specified book')

    def test_edit_non_existence_book_fails(self):
        '''This endpoint updates information for a given book'''
        new_info = {'id': -1, 'title': 'Learn Java the Hard way',
                    'author': 'Meshack'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_info), content_type='application/json')

        self.assertEqual(resp.status_code, 404,
                         msg="Not found")

        # load data from response object
        data = json.loads(resp.get_data().decode('utf-8'))

        # extract the message
        msg = data['message']

        self.assertEqual(msg, 'book with that id not found',
                         msg='Should not update book that does not exist')

    def test_edit_book_using_empty_fields_fail(self):
        '''This endpoint updates information for a given book'''
        new_info = {'id': -1, 'title': '', 'author': 'Meshack'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_info), content_type='application/json')

        self.assertEqual(resp.status_code, 400,
                         msg="Endpoint should be reachable")

        data = json.loads(resp.get_data().decode('utf-8'))
        msg = data['message']

        self.assertEqual(msg, 'Ensure to use json format and fill all fields',
                         msg='All fields must be filled when updating book information')

    def test_book_fields_are_strings_only(self):
        '''This endpoint updates information for a given book'''
        new_info = {'id': 0, 'title': '09870957jgjh', 'author': 'Meshack'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_info), content_type='application/json')

        data = json.loads(resp.get_data().decode('utf-8'))
        msg = data['message']

        self.assertEqual(resp.status_code, 400,
                         msg="Bad format")

        

        self.assertEqual(msg, 'Do not use numbers in your fields',
                         msg='Fields can only contain strings')


if __name__ == '__main__':
    unittest.main()
