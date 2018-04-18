import json
import unittest

from application import *


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

    def test_a_user_can_borrow_a_book(self):
        """Tests that a logged in user can borrow an existing book."""
        response = self.app.post('/api/v1/users/books/67890', headers={'content_type': 'application/json',
                                                                       'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 200)
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertTrue(received_data['message'])

    def test_cannot_borrow_book_marked_already_borrowed(self):
        """Tests that a book cannot be borrowed more than once unless returned first
        We attempt to borrow a book twice.

        """
        self.app.post('/api/v1/users/books/67890', headers={'content_type': 'application/json',
                                                            'Authorization': 'Bearer {}'.format(self.token)})
        response = self.app.post('/api/v1/users/books/67890', headers={'content_type': 'application/json',
                                                                       'Authorization': 'Bearer {}'.format(self.token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['Message'], 'Book is not available for renting')

    def test__user_cannot_borrow_non_existing_book(self):
        """Tests user cannot a borrow a book that does not exist."""

        response = self.app.post('/api/v1/users/books/-1', headers={'content_type': 'application/json',
                                                                    'Authorization': 'Bearer {}'.format(self.token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['Message'], 'Book with that isbn is not available')

    def test_user_without_valid_token_cannot_borrow_book(self):
        """Tests user with an invalid authorization token cannot a borrow a book
        Take a valid token and append any character to it before sending it to the endpoint.

        """
        response = self.app.post('/api/v1/users/books/1', headers={'content_type': 'application/json',
                                                                   'Authorization': 'Bearer {}h'.format(self.token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['msg'], 'Signature verification failed')

    def test_only_logged_in_user_can_borrow_book(self):
        """Tests user who tries to borrow a book without providing an authorization token."""

        response = self.app.post('/api/v1/users/books/1', headers={'content_type': 'application/json'})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['msg'], 'Missing Authorization Header')


if __name__ == '__main__':
    unittest.main()
