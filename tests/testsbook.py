from run import *
import unittest
import json

from base64 import b64encode


class TestsBook(unittest.TestCase):

    def setUp(self):
            # create new user
        self.app = app
        self.app = self.app.test_client()

        # Prepare for testing;set up variables
        self.users_table = users_table
        # Login first to get token
        url = 'http://localhost:5000/api/v1/auth/'

        user_data = {'username': 'mbuvi', 'password': 'meshack'}

        headers = {}
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] + ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        # connect to the endpoint for login
        response = self.app.get(
            url + 'login', content_type='application/json', headers=headers)
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token = received_data['token']


        self.BASE_URL = 'http://localhost:5000/api/v1/users/books/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app = None
        self.BASE_URL = None

    def test_user_can_borrow_a_book(self):
        # username and book id to send to the API endpoint
        username_book_id = {"username": "mbuvi", "id": 1}

        response = self.app.post(self.BASE_URL + '%s' % username_book_id['id'],
                             data=json.dumps(username_book_id), content_type='application/json')

        received_data = json.loads(response.get_data().decode('utf-8'))
        print(received_data)

        self.assertEqual(received_data, rental_details,
                         msg="Should allocate the book to user")

    def test_unexisting_user_cannot_borrow_book(self):
        # username and book id to send to the API endpoint
        data = {"username": "mbuvigsg", "id": len(books_in_api) - 1}

        resp = self.app.post(self.BASE_URL + '%s' % data['id'],
                             data=json.dumps(data), content_type='application/json')

        recv = json.loads(resp.get_data().decode('utf-8'))
        msg = recv['Message']

        self.assertEqual(msg, 'No user with the username provided',
                         msg="Should not allocate book to users who are non-existing")

    def test__user_cannot_borrow_non_existing_book(self):
        # username and book id to send to the API endpoint
        data = {"username": "mbuvi", "id": -1}

        resp = self.app.post(self.BASE_URL + '%s' % data['id'],
                             data=json.dumps(data), content_type='application/json')

        recv = json.loads(resp.get_data().decode('utf-8'))

        msg = 'Book with that Id is not available'

        self.assertEqual(msg, 'Book with that Id is not available',
                         msg="Should not allocate book to users who are non-existed")


if __name__ == '__main__':
    unittest.main()
