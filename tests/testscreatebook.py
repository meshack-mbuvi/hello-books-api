from run import *
import unittest
import json
from instance.config import configuration
from application.views import books_in_api

from base64 import b64encode


class TestsBook(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()

        url = '/api/v1/auth/'
        # Login as an admin
        user_data = {'username': 'mbuvi', 'password': 'meshack'}
        response = self.app.post(url + 'login', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token = received_data['token']

        # Login as a normal user
        user_data = {'username': 'mbuv', 'password': 'meshack'}
        response = self.app.post(url + 'login', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token1 = received_data['token']
        self.BASE_URL = '/api/v1/books/'

    def tearDown(self):
        """Clean our environment before leaving"""
        self.app = None
        self.BASE_URL = None

    def test_can_create_a_book(self):
        """Test can create a new book item
        compare the number of books before and after creating a new book item"""

        book_data = {'title': 'Learn Android in Two days', 'author': 'Meshack Mbuvi'}
        initial_number_of_books = len(books_in_api)
        self.app.post(self.BASE_URL, data=json.dumps(book_data), content_type='application/json',
                      headers={'Authorization': 'Bearer {}'.format(self.token)})
        number_of_books_after = len(books_in_api)
        self.assertTrue(number_of_books_after > initial_number_of_books)

    def test_cannot_create_a_book_without_details(self):
        """Test cannot create a new book item without providing details
        compare the number of books before and after creating a new book item"""

        book_data= {'title': '', 'author': 'Meshack Mbuvi'}
        initial_number_of_books = len(books_in_api)
        self.app.post(self.BASE_URL, data=json.dumps(book_data), content_type='application/json',
                      headers={'Authorization': 'Bearer {}'.format(self.token)})
        number_of_books_after = len(books_in_api)
        self.assertTrue(number_of_books_after == initial_number_of_books)

    def test_cannot_create_a_book_without_being_logged_in(self):
        """Test user cannot create a new book item if not logged in
        compare the number of books before and after creating a new book item"""

        book_data= {'title': 'Learn android programming', 'author': 'Meshack Mbuvi'}
        initial_number_of_books = len(books_in_api)
        self.app.post(self.BASE_URL, data=json.dumps(book_data), content_type='application/json')
        number_of_books_after = len(books_in_api)
        self.assertTrue(number_of_books_after == initial_number_of_books)

    def test_only_an_admin_can_create_a_new_book(self):
        """Test cannot create a new book item without providing details
        compare the number of books before and after creating a new book item"""

        book_data= {'title': 'Learn and learn', 'author': 'Meshack Mbuvi'}
        initial_number_of_books = len(books_in_api)
        self.app.post(self.BASE_URL, data=json.dumps(book_data), content_type='application/json',
                      headers={'Authorization': 'Bearer {}'.format(self.token1)})
        number_of_books_after = len(books_in_api)
        self.assertTrue(number_of_books_after == initial_number_of_books)
