import json
import unittest

from application import *
from application.models.bookmodels import *


class TestsBook(unittest.TestCase):

    def setUp(self):
        """ prepares variables to be used in the testcases.
        Register a user; an admin and use the admin details to add a new book to database.

        """
        self.app = app_config('testing')
        self.app = self.app.test_client()
        db.create_all()
        url = '/api/v1/auth/'

        # create an admin and log him in
        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya', 'admin': 'True'}
        self.app.post(url + 'register', data=json.dumps(user_data), content_type='application/json')

        user_login = {'username': 'Jacob', 'password': 'munyasya'}
        response = self.app.post(url + 'login', data=json.dumps(user_login), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token = received_data['token']

        book_data = {'isbn': '67890', 'title': 'Learn Android in Two days', 'author': 'Meshack Mbuvi'}
        self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json',
                      headers={'Authorization': 'Bearer {}'.format(self.token)})

    def tearDown(self):
        """Clean our environment before leaving."""
        self.app = None
        db.session.remove()
        db.drop_all()

    def test_user_can_get_her_borrowing_history(self):
        """Borrow a book and return it, try to get borrowing history."""
        self.app.post('/api/v1/users/books/67890', headers={'content_type': 'application/json',
                                                            'Authorization': 'Bearer {}'.format(self.token)})
        # Return borrowed book
        self.app.put('/api/v1/users/books/67890', headers={'content_type': 'application/json',
                                                           'Authorization': 'Bearer {}'.format(self.token)})
        self.app.post('/api/v1/users/books/67890', headers={'content_type': 'application/json',
                                                            'Authorization': 'Bearer {}'.format(self.token)})
        # get borrowing history
        response = self.app.get('/api/v1/users/books', headers={'content_type': 'application/json',
                                                                'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 200)
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(len(received_data), 2)

    def test_user_can_get_many_books_on_her_history(self):
        """Borrow a book and return it several times, try to get borrowing history."""
        for number in range(10):
            self.app.post('/api/v1/users/books/67890', headers={'content_type': 'application/json',
                                                                'Authorization': 'Bearer {}'.format(self.token)})
            # Return borrowed book
            self.app.put('/api/v1/users/books/67890', headers={'content_type': 'application/json',
                                                               'Authorization': 'Bearer {}'.format(self.token)})

        # get borrowing history
        response = self.app.get('/api/v1/users/books', headers={'content_type': 'application/json',
                                                                'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 200)
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(len(received_data), 10)
