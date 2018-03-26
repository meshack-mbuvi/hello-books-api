import unittest
import json

from run import app
from application.books.models import *
from application.books.views import books_in_api


class BookAPITests(unittest.TestCase):

    def setUp(self):
        # Prepare for testing;set up variables
        self.app = app
        # create books(instances of Books class) for testing.
        self.bk = Book(1, 'Test Driven Development', 'Kent Beck')
        books_in_api.append(self.bk)

        self.bk1 = Book(3, 'Python Programming','Peter Carl')
        self.bk4 = Book(4, 'Flask API tutorial','John Kell')

        books_in_api.append(self.bk1)
        books_in_api.append(self.bk4)

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
        test_item = {'id': 3,'author': 'Peter Carl','title': 'Python Programming' }

        # test_item should be in the list
        self.assertTrue(test_item in data, msg='Should retrieve items')

    


if __name__ == '__main__':
    unittest.main()
