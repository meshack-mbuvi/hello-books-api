import json
import unittest

from application import *


class TestsBook(unittest.TestCase):

    def setUp(self):
        """ prepares variables to be used in the testcases.
        Register two users; an admin and normal user. Log in both users to get their authentication tokens.
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
        """Clean our environment before leaving."""
        self.app = None
        db.session.remove()
        db.drop_all()

    def test_edit_book(self):
        """Try to edit data for an existing book."""

        new_data = {'title': 'Learn Java the Hard way', 'author': 'Meshack'}
        response = self.app.put('/api/v1/books/67890', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 200, msg="Book should be modified")
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data, new_data)

    def test_cannot_edit_book_without_authorization_token(self):
        """Try editing book information without providing authentication token."""

        new_data = {'title': 'Learn Java the Hard way', 'author': 'Meshack'}
        response = self.app.put('/api/v1/books/67890', data=json.dumps(new_data), content_type='application/json')
        self.assertEqual(response.status_code, 401, msg="Endpoint should be reachable")

    def test_only_an_administrator_can_edit_book_details(self):
        """Attempting to edit book data using authentication token for a normal user."""

        new_data = {'title': 'Learn Java the Hard way', 'author': 'Meshack'}
        response = self.app.put('/api/v1/books/67890', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token1)})
        self.assertEqual(response.status_code, 401, msg="Endpoint should be reachable")

    def test_edit_non_existence_book_fails(self):
        """Try editing data for a book that does not exist with the systme. """

        new_data = {'title': 'Learn Java the Hard way', 'author': 'Meshack'}
        response = self.app.put('/api/v1/books/-1', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 404, msg="Book with given id does not exist")

    def test_edit_book_using_empty_fields_fail(self):
        """Attempt to edit book data by providing empty fields. """

        new_data = {'title': '', 'author': ''}
        response = self.app.put('/api/v1/books/67890', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 400, msg="Book 'title' and/or 'author' must be non-empty strings")

    def test_book_fields_are_strings_only(self):
        """Try editing book data by providing fields with digits."""

        new_data = {'title': '344tgsdgv', 'author': 'sdgqw34'}
        response = self.app.put('/api/v1/books/67890', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 400, msg="Book 'title' and/or 'author' must be non-empty strings")

    def test_failure_to_provide_isbn_or_title_or_author_fields_fail(self):
        """Try editing book data without providing the required fields. """

        new_data = {'nottitle': 'Mesh', 'notauthor': 'Me and you are developers'}
        response = self.app.put('/api/v1/books/67890', data=json.dumps(new_data), content_type='application/json',
                                headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 400, msg="Book 'title' and/or 'author' must be provided")


if __name__ == '__main__':
    unittest.main()
