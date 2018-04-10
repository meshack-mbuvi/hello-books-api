from base64 import b64encode
from run import *
import unittest
import json
from instance.config import configuration


class TestsBook(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()

    def tearDown(self):
        """Clean our environment before leaving"""
        self.app = None

    def test_can_retrieve_all_books(self):
        """ Tests users can retrieve books
        checks the status code returned from from the endpoint
        """
        response = self.app.get('/api/v1/books/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_retrieve_a_single_item(self):
        """ Tests user can retrieve a single book
        Done by checking the status code of the response from the endpoint
        """
        response = self.app.get('/api/v1/books/1')
        self.assertEqual(response.status_code, 200)

    def test_retrieval_of_a_non_existing_book_fails(self):
        """ Tests tha user cannot retrieve a book that does not exist.
        Assumes negative book ids do not exist. This test holds for any other non-existing ids in the api"""
        resp = self.app.get('/api/v1/books/-1')
        self.assertEqual(resp.status_code, 404, msg='Should not retrieve a book that does not exist.')


if __name__ == '__main__':
    unittest.main()
