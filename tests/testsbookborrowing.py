from run import *
import unittest
import json

class TestsBook(unittest.TestCase):

    def setUp(self):
            # create new user
        self.app = app
        self.app = self.app.test_client()

        # Prepare for testing;set up variables
        self.user = User(username="mbuvi", password="mesh")
        users_table[len(users_table) + 1] = self.user.getdetails()
        self.users_table = users_table

        # add a book to the app
        book = Book('Marcos', 'Learn Android the Hard way')
        books_in_api[len(books_in_api)] = book.getdetails()

        self.BASE_URL = 'http://localhost:5000/api/v1/auth/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        self.users_table = None

    def test_user_can_borrow_a_book(self):
        # username and book id to send to the API endpoint
        data = {"username": "mbuvi", "id": len(books_in_api) - 1}

        resp = self.app.post('http://localhost:5000/api/v1/users/books/',
                             data=json.dumps(data), content_type='application/json')
        if resp.status_code == 404:
            return 1
        recv = json.loads(resp.get_data().decode('utf-8'))

        rental_details = {'id': recv['book_id'], 'username': recv['username']}

        self.assertEqual(data, rental_details,
                         msg="Should allocate the book to user")


if __name__ == '__main__':
    unittest.main()
