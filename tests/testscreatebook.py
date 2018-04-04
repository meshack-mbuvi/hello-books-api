from run import *
import unittest
import json
from instance.config import configuration

from base64 import b64encode


class TestsBook(unittest.TestCase):

    def setUp(self):
            # create new user
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()
        # Login first to get token
        url = '/api/v1/auth/'

        user_data = {'username': 'mercy', 'password': 'macks'}

        headers = {}
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] + ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        # connect to the endpoint for login
        response = self.app.get(
            url + 'login', content_type='application/json', headers=headers)
        received_data = json.loads(response.get_data().decode('utf-8'))

        self.token = received_data['token']


        self.BASE_URL = '/api/v1/books/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app = None
        self.BASE_URL = None

    def test_can_create_a_book(self):
        '''Test can create a new book item
        compare the number of books before and after creating a new book item'''
        book_info= {'title': 'Learn Android in Two days', 'author': 'Meshack Mbuvi'}

        initial_number_of_books = len(books_in_api)

        response = self.app.post(self.BASE_URL,
                             data=json.dumps(book_info), content_type='application/json')
        number_of_books_after = len(books_in_api)        

        self.assertTrue(number_of_books_after > initial_number_of_books)

    def test_cannot_create_a_book_without_details(self):
        '''Test cannot create a new book item without providing details
        compare the number of books before and after creating a new book item'''
        book_info= {'title': '', 'author': 'Meshack Mbuvi'}

        initial_number_of_books = len(books_in_api)

        response = self.app.post(self.BASE_URL,
                             data=json.dumps(book_info), content_type='application/json')
        number_of_books_after = len(books_in_api)        

        self.assertTrue(number_of_books_after == initial_number_of_books)