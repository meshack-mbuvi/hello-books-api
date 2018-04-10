from run import *
import unittest
import json
from instance.config import configuration


class TestsBook(unittest.TestCase):

    def setUp(self):
        """ create new user"""
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()
        # Login first to get token
        url = '/api/v1/auth/'
        user_data = {'username': 'mbuvi', 'password': 'meshack'}
        # login to get authentication token
        response = self.app.post(url + 'login', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token = received_data['token']

    def tearDown(self):
        """Clean our environment before leaving"""
        self.app = None

    def test_a_user_can_borrow_a_book(self):
        """Tests that a logged in user can borrow an existing book"""
        response = self.app.post('/api/v1/users/books/1', headers={'content_type': 'application/json',
                                                                   'Authorization': 'Bearer {}'.format(self.token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['available'], False)

    def test_cannot_borrow_book_marked_as_unavailable(self):
        """Tests a book marked as unavailable cannot be borrowed"""
        response = self.app.post('/api/v1/users/books/1', headers={'content_type': 'application/json',
                                                                   'Authorization': 'Bearer {}'.format(self.token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['Message'], 'Book is not available for renting')

    def test__user_cannot_borrow_non_existing_book(self):
        """Tests user cannot a borrow a book that does not exist"""
        response = self.app.post('/api/v1/users/books/-1', headers={'content_type': 'application/json',
                                                                    'Authorization': 'Bearer {}'.format(self.token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['Message'], 'Book with that Id is not available')

    def test_user_without_valid_token_cannot_borrow_book(self):
        """Tests user with an invalid authorization token cannot a borrow a book
        Take a valid token and append any character to it before sending it to the endpoint"""
        response = self.app.post('/api/v1/users/books/1', headers={'content_type': 'application/json',
                                                                   'Authorization': 'Bearer {}h'.format(self.token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['msg'], 'Signature verification failed')

    def test_only_logged_in_user_can_borrow_book(self):
        """Tests user who tries to borrow a book without providing an authorization token"""
        response = self.app.post('/api/v1/users/books/1', headers={'content_type': 'application/json'})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['msg'], 'Missing Authorization Header')


if __name__ == '__main__':
    unittest.main()
