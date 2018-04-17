import json
import unittest

from run import *


class TestsBook(unittest.TestCase):

    def setUp(self):
        """ prepares variables to be used in the testcases.
        Register a user; an admin and use the admin details to add a new book to database.

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
        book_data = {'isbn': '67890', 'title': 'Learn Android in Two days', 'author': 'Meshack Mbuvi'}
        self.app.post('/api/v1/books/', data=json.dumps(book_data), content_type='application/json',
                      headers={'Authorization': 'Bearer {}'.format(self.token)})

    def tearDown(self):
        """Clean our environment before leaving"""
        self.app = None
        db.session.remove()
        db.drop_all()

    def test_can_retrieve_all_books(self):
        """ Tests users can retrieve books
        checks the status code returned from from the endpoint.

        """
        response = self.app.get('/api/v1/books/')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        book_info = received_data['67890']

        self.assertEqual(book_info['title'], "Learn Android in Two days")

    def test_user_can_retrieve_a_single_item(self):
        """ Tests user can retrieve a single book
        Done by checking the status code of the response from the endpoint

        """
        response = self.app.get('/api/v1/books/67890')
        self.assertEqual(response.status_code, 200)

    def test_retrieval_of_a_non_existing_book_fails(self):
        """ Tests tha user cannot retrieve a book that does not exist.
        Assumes negative book ids do not exist. This test holds for any other non-existing ids in the api

        """
        resp = self.app.get('/api/v1/books/-167687')
        self.assertEqual(resp.status_code, 404, msg='Should not retrieve a book that does not exist.')


if __name__ == '__main__':
    unittest.main()
