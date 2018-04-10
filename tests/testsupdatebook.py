from run import *
import unittest
import json
from instance.config import configuration
from application.views import users_table
from application.models.usermodel import User


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

    def tearDown(self):
        """Clean our environment before leaving"""
        self.app = None
        self.BASE_URL = None
        self.users_table = None

    def test_edit_book(self):
        """Test that a user can edit book information
        """
        new_data = {'title': 'Learn Java the Hard way', 'author': 'Meshack'}
        response = self.app.put('/api/v1/books/1', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 200, msg="Book should be modified")

    def test_cannot_edit_book_without_authorization_token(self):
        """Test that a user can edit book information
        """
        new_data = {'title': 'Learn Java the Hard way', 'author': 'Meshack'}
        response = self.app.put('/api/v1/books/1', data=json.dumps(new_data), content_type='application/json')
        self.assertEqual(response.status_code, 401, msg="Endpoint should be reachable")

    def test_only_an_administrator_can_edit_book_details(self):
        """Test that a normal user cannot edit book information
        Done by using authorization token for a normal user to edit book information
        """
        new_data = {'title': 'Learn Java the Hard way', 'author': 'Meshack'}
        response = self.app.put('/api/v1/books/1', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token1)})
        self.assertEqual(response.status_code, 401, msg="Endpoint should be reachable")

    def test_edit_non_existence_book_fails(self):
        """Test that user cannot modify data for a book that does not exist
        Assumes that book ids take non-negative values. This test succeeds if id is negative
        or if it exceeds the highest key for the books"""
        new_data = {'title': 'Learn Java the Hard way', 'author': 'Meshack'}
        response = self.app.put('/api/v1/books/-1', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 404, msg="Book with given id does not exist")

    def test_edit_book_using_empty_fields_fail(self):
        """Test that book title and /or author must be provided in order to update book data"""

        new_data = {'title': '', 'author': ''}
        response = self.app.put('/api/v1/books/1', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 400, msg="Book 'title' and/or 'author' must be non-empty strings")

    def test_book_fields_are_strings_only(self):
        """Test that book data fields can only be non-empty strings but not integers or a mixture of both"""
        new_data = {'title': '344tgsdgv', 'author': 'sdgqw34'}
        response = self.app.put('/api/v1/books/1', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 400, msg="Book 'title' and/or 'author' must be non-empty strings")

    def test_failure_to_provide_title_or_author_fields_fail(self):
        """Test that book data fields can only be non-empty strings but not integers or a mixture of both"""
        new_data = {'nottitle': 'Mesh', 'notauthor': 'Me and you are developers'}
        response = self.app.put('/api/v1/books/1', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 400, msg="Book 'title' and/or 'author' must be provided")



if __name__ == '__main__':
    unittest.main()
