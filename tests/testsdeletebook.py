from run import *
import unittest
import json
from instance.config import configuration
from application.views import books_in_api


class TestsBook(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()
        # Login to get token
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

    def tearDown(self):
        """Clean our environment before leaving"""
        self.app = None
        self.users_table = None

    def test_delete_item(self):
        """ Test user can delete a book
        compares the number of books before and after deletion
        """
        no_of_books_before = len(books_in_api)
        response = self.app.delete('/api/v1/books/4', headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 200)
        no_of_books_after = len(books_in_api)
        self.assertTrue(no_of_books_before > no_of_books_after, msg='The api should delete a book')

    def test_delete_non_existence_book_fails(self):
        """Checks for status code returned when user attempts to delete a book that does not exist.
        It assumes all book ids are from 0 upwards; no negative ids"""

        response = self.app.delete('/api/v1/books/-1', headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 404)

    def test_only_admin_can_delete_a_book(self):
        """Uses login details for a user who is a non-administrator"""

        response = self.app.delete('/api/v1/books/3', headers={'Authorization': 'Bearer {}'.format(self.token1)})
        self.assertEqual(response.status_code, 401)

    def test_user_not_logged_in_cannot_delete_a_book(self):
        """Delete a book without providing authorization token"""
        response = self.app.delete('/api/v1/books/3')
        self.assertEqual(response.status_code, 401)

    def test_user_cannot_delete_a_book_if_its_borrowed(self):
        """Delete a book without providing authorization token
        We borrow a book and then attempt to delete it"""
        self.app.post('/api/v1/users/books/1', headers={'content_type': 'application/json',
                                                                   'Authorization': 'Bearer {}'.format(self.token)})

        response = self.app.delete('/api/v1/books/1', headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 304)


if __name__ == '__main__':
    unittest.main()
