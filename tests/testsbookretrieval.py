from base64 import b64encode
from run import *
import unittest
import json


class TestsBook(unittest.TestCase):

    def setUp(self):
            # create new user
        self.app = app
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

    def test_get_all_books(self):
        ''' test the api can retrieve books
        '''
        resp = self.app.get(self.BASE_URL)
        self.assertEqual(resp.status_code, 200,
                         msg='Should retrieve data from the api.')

        data = json.loads(resp.get_data().decode('utf-8'))

        # test_item should be in the list
        self.assertTrue(data, msg='Should retrieve items')

    def test_get_a_single_item(self):
        ''' test the api can retrieve books
        '''
        item_id = 0
        resp = self.app.get(self.BASE_URL + '%d/' % item_id)
        data = json.loads(resp.get_data().decode('utf-8'))

        self.assertEqual(resp.status_code, 200,
                         msg='Should retrieve data from the api.')

        # test_item should be in the list
        self.assertTrue(data,
                        msg='Should retrieve an item with id = item_id')

    def test_get_a_non_existing_book_fails(self):
        ''' test the api can retrieve books
        '''
        item_id = -1
        resp = self.app.get(self.BASE_URL + '%d/' % item_id)
        data = json.loads(resp.get_data().decode('utf-8'))

        self.assertEqual(resp.status_code, 404,
                         msg='Should not retrieve a book that does not exist.')

        # test_item should be in the list
        self.assertTrue(data,
                        msg='Should not retrieve a non existing book.')


if __name__ == '__main__':
    unittest.main()
