from base64 import b64encode
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

        self.BASE_URL = '/api/v1/books/'

    def tearDown(self):
        '''Clean our environment before leaving'''
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
        book_id = 1
        resp = self.app.get(self.BASE_URL + '%d' % book_id)
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
        resp = self.app.get(self.BASE_URL + '%d' % item_id)
        data = json.loads(resp.get_data().decode('utf-8'))

        self.assertEqual(resp.status_code, 404,
                         msg='Should not retrieve a book that does not exist.')
        

        # test_item should be in the list
        self.assertEqual(data ,'Book not found',
                        msg='Should not retrieve a non existing book.')


if __name__ == '__main__':
    unittest.main()
