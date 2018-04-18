import json
import unittest

from application import *


class TestsBook(unittest.TestCase):

    def setUp(self):
        """ prepares variables to be used in the testcases.
        Register two users; an admin and normal user, log them in to get their authentication tokens.
        Use admin details to add a new book to database.

        """
        self.app = app_config('testing')
        self.app = self.app.test_client()
        db.create_all()

        url = '/api/v1/auth/'

        # create an admin and log him in
        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya', 'admin': 'True'}
        self.app.post(url + 'register', data=json.dumps(user_data), content_type='application/json')

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'James',
                     'password': 'munyasya', }
        self.app.post(url + 'register', data=json.dumps(user_data), content_type='application/json')

        user_login = {'username': 'Jacob', 'password': 'munyasya'}
        response = self.app.post(url + 'login', data=json.dumps(user_login), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token = received_data['token']

        user_login = {'username': 'James', 'password': 'munyasya'}
        response = self.app.post(url + 'login', data=json.dumps(user_login), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token1 = received_data['token']
        book_data = {'isbn': '67890', 'title': 'Learn Android in Two days', 'author': 'Meshack Mbuvi'}
        self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json',
                      headers={'Authorization': 'Bearer {}'.format(self.token)})

    def tearDown(self):
        """Clean our environment before leaving"""
        self.app = None
        db.session.remove()
        db.drop_all()

    def test_delete_item(self):
        """ Attempt to delete a book."""

        response = self.app.delete('/api/v1/books/67890', headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existence_book_fails(self):
        """Try to delete a book with negative isbn."""

        response = self.app.delete('/api/v1/books/098', headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 404)

    def test_only_admin_can_delete_a_book(self):
        """attempt to delete a book using credentials for a normal user."""

        response = self.app.delete('/api/v1/books/3', headers={'Authorization': 'Bearer {}'.format(self.token1)})
        self.assertEqual(response.status_code, 401)

    def test_user_not_logged_in_cannot_delete_a_book(self):
        """Attempt to delete a book without providing authorization token."""

        response = self.app.delete('/api/v1/books/3')
        self.assertEqual(response.status_code, 401)

    def test_user_cannot_delete_a_book_if_its_borrowed(self):
        """Borrow a book and then try to delete it."""
        self.app.post('/api/v1/users/books/67890', headers={'content_type': 'application/json',
                                                            'Authorization': 'Bearer {}'.format(self.token)})
        response = self.app.delete('/api/v1/books/67890', headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 304)


if __name__ == '__main__':
    unittest.main()
