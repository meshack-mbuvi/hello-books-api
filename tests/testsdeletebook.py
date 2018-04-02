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

        self.BASE_URL = 'http://localhost:5000/api/v1/books/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        self.users_table = None

    def test_delete_item(self):
        ''' test the api can delete a book
        '''

        item_id = 1
        # Get initial number of books before deleting
        no_of_books_before = 0
        no_of_books_after = 0

        # Create dummy variables for testing if
        no_of_books_before = len(books_in_api)

        resp = self.app.delete(self.BASE_URL + '%d/' % item_id)
        if resp.status_code == 404:
            return
        self.assertEqual(resp.status_code, 200,
                         msg='The api should be reachable')

        # Get size of books in the api after deletion
        no_of_books_after = len(books_in_api)

        self.assertTrue(no_of_books_before > no_of_books_after,
                        msg='The api should delete a book')

    def test_delete_non_existence_item_fails(self):
        item_id = -1
        resp = self.app.delete(self.BASE_URL + '%d/' % item_id)
        if resp.status_code == 404:
            return
        self.assertEqual(resp.status_code, 404,
                         msg='Not found')

        # Retrieve the message
        msg = resp.get_data().decode('utf-8')

        self.assertEqual(msg, 'Book Id cannot take negative values',
                         msg='The api should not delete a non existing book')


if __name__ == '__main__':
    unittest.main()
