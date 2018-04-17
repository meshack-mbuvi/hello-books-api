import json
import unittest

from application.models.bookmodels import *
from run import *


class TestsBook(unittest.TestCase):

    def setUp(self):
        """
        creates two users; an admin and a normal user, and logs them in to get their authentication tokens.
        """
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()
        db.create_all()

        url = '/api/v1/auth/'

        # create an admin and log him in
        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya', 'admin': 'True'}
        self.app.post(url + 'register', data=json.dumps(user_data), content_type='application/json')
        user_data = {'username': 'Jacob', 'password': 'munyasya'}
        response = self.app.post(url + 'login', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token = received_data['token']

        # create a normal user and log him in
        user_data = {'firstname': 'Meshack', 'secondname': 'mbuvi', 'email': 'mbuvi@gmail.com', 'username': 'mbuvi',
                     'password': 'meshack1'}
        self.app.post(url + 'register', data=json.dumps(user_data), content_type='application/json')
        user_data = {'username': 'mbuvi', 'password': 'meshack1'}
        response = self.app.post(url + 'login', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token1 = received_data['token']

    def tearDown(self):
        """Clean our environment before leaving."""
        self.app = None
        self.token = None
        self.token1 = None
        db.session.remove()
        db.drop_all()

    def test_can_create_a_book(self):
        """Create a new book.
        compare the number of books before and after creating a new book item.

        """
        books = db.session.query(Book).all()
        initial_number_of_books = len(books)
        book_data = {'isbn': '67890', 'title': 'Learn Android in Two days', 'author': 'Meshack Mbuvi'}
        self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json',
                      headers={'Authorization': 'Bearer {}'.format(self.token)})
        books = db.session.query(Book).all()
        number_of_books_after = len(books)
        self.assertTrue(number_of_books_after > initial_number_of_books)

    def test_cannot_create_a_book_that_exists(self):
        """Attempt to create an existing book."""

        book_data = {'isbn': '67890', 'title': 'Learn Android in Two days', 'author': 'Meshack Mbuvi'}
        self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json',
                      headers={'Authorization': 'Bearer {}'.format(self.token)})
        response = self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json',
                                 headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 409)

    def test_book_title_and_author_can_be_strings_only(self):
        """Attempt to create a new book with title and author having digits. """

        book_data = {'isbn': '67890', 'title': '433e', 'author': '098yhjbnwke'}
        response = self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json',
                                 headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 400)

    def test_cannot_create_a_book_without_author_or_title_details(self):
        """Attempt to create a new book without providing book title and author information."""

        book_data = {'isbn': '67890', 'titlefghdf': 'nfgnfn', 'authorghs': 'Meshack Mbuvi'}
        response = self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json',
                                 headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(response.status_code, 400)

    def test_cannot_create_a_book_without_being_logged_in(self):
        """Attempt to create a book without providing authorization token. """

        book_data = {'isbn': '67890', 'title': 'Learn android programming', 'author': 'Meshack Mbuvi'}
        response = self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_only_an_admin_can_create_a_new_book(self):
        """Attempt to create a book using authentication token for a normal user."""

        book_data = {'isbn': '67890', 'title': 'Learn and learn', 'author': 'Meshack Mbuvi'}
        response = self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json',
                                 headers={'Authorization': 'Bearer {}'.format(self.token1)})
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
