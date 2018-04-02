from run import *
import unittest
import json
from instance.config import configuration


class TestsBook(unittest.TestCase):

    def setUp(self):
            # create new user
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()

        # Prepare for testing;set up variables
        self.user = User(username="mbuvi", password="mesh")
        users_table[len(users_table) + 1] = self.user.getdetails()

        self.users_table = users_table

        # add a book to the app
        book = Book('Marcos', 'Learn Android the Hard way')
        books_in_api[len(books_in_api)] = book.getdetails()

        self.BASE_URL = 'http://localhost:5000/api/v1/users/books/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        self.users_table = None

    def test_user_can_borrow_a_book(self):
        # username and book id to send to the API endpoint
        data = {"username": "mbuvi", "id": 0}

        resp = self.app.post(self.BASE_URL,
                             data=json.dumps(data), content_type='application/json')

        recv = json.loads(resp.get_data().decode('utf-8'))

        rental_details = {'id': recv['book_id'], 'username': recv['username']}

        self.assertEqual(data, rental_details,
                         msg="Should allocate the book to user")

    def test_unexisting_user_cannot_borrow_book(self):
        # username and book id to send to the API endpoint
        data = {"username": "mbuvigsg", "id": len(books_in_api) - 1}

        resp = self.app.post(self.BASE_URL,
                             data=json.dumps(data), content_type='application/json')

        recv = json.loads(resp.get_data().decode('utf-8'))
        msg = recv['Message']

        self.assertEqual(msg, 'No user with the username provided',
                         msg="Should not allocate book to users who are non-existing")

    def test__user_cannot_borrow_non_existing_book(self):
        # username and book id to send to the API endpoint
        data = {"username": "mbuvi", "id": -1}

        resp = self.app.post(self.BASE_URL,
                             data=json.dumps(data), content_type='application/json')

        recv = json.loads(resp.get_data().decode('utf-8'))

        msg = 'Book with that Id is not available'

        self.assertEqual(msg, 'Book with that Id is not available',
                         msg="Should not allocate book to users who are non-existed")


if __name__ == '__main__':
    unittest.main()
