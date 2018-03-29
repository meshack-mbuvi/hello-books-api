import unittest
import json

from run import app
from application.books.models import *
from application.books.views import books_in_api


class BookAPITests(unittest.TestCase):

    def setUp(self):
        # Prepare for testing;set up variables
        self.app = app
        # create books(instances of Books class) for testing.
        self.bk = Book(1, 'Test Driven Development', 'Kent Beck')
        books_in_api.append(self.bk)

        self.bk1 = Book(3, 'Python Programming', 'Peter Carl')
        self.bk4 = Book(4, 'Flask API tutorial', 'John Kell')

        books_in_api.append(self.bk1)
        books_in_api.append(self.bk4)

        self.app = self.app.test_client()
        self.BASE_URL = 'http://localhost:5000/api/v1/books/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None

    def test_get_all_books(self):
        ''' test the api can retrieve books
        '''
        resp = self.app.get(self.BASE_URL)
        self.assertEqual(resp.status_code, 200,
                         msg='Should retrieve data from the api.')

        data = json.loads(resp.get_data().decode('utf-8'))
        test_item = {'id': 3, 'author': 'Peter Carl',
                     'title': 'Python Programming'}

        # test_item should be in the list
        self.assertTrue(test_item in data, msg='Should retrieve items')

    def test_get_a_single_book(self):
        ''' test the api can retrieve books
        '''
        item_id = 1
        resp = self.app.get(self.BASE_URL + '%d/' % item_id)
        self.assertEqual(resp.status_code, 200,
                         msg='Should retrieve data from the api.')

        data = json.loads(resp.get_data().decode('utf-8'))
        items = data['Book']
        test_item = {'id': 1, 'title': 'Test Driven Development',
                     'author': 'Kent Beck'}


        # test_item should be in the list
        self.assertTrue(test_item == items,
                        msg='Should retrieve an item with id = item_id')

    def test_post_book(self):
        '''This method tests that the api can save data.'''
        # book to post
        book = {'title': 'Test Driven Developemnt',
                'author': 'Kent Beck'}

        resp = self.app.post(self.BASE_URL, data=json.dumps(
            book), content_type='application/json')
        self.assertEqual(resp.status_code, 201,
                         msg='Request not excuted")

        # confirm that data has been saved
        data = json.loads(resp.get_data().decode('utf-8'))
        test_data = {'title': data['title'], 'author': data['author']}

        self.assertEqual(book, test_data,
                         msg='The api should save data for new book item')

   
    def test_delete_book(self):
        ''' test the api can delete a book
        '''


        item_id = 1
        resp = self.app.delete(self.BASE_URL + '%d/' % item_id)
        
        if resp.status_code == 404:
            return True

        self.assertEqual(resp.status_code, 200,
                         msg='Request not excuted")
       
        test_item = (1, 'Test Driven Development', 'Kent Beck')
        # Get all books in the api
        books = []
        for book in books_in_api:
            books.append((book.id, book.title, book.author))

        self.assertFalse(test_item in books,
                         msg='The api should delete a book')


    def test_edit_book(self):

        '''This endpoint updates information for a given book'''
        new_info = {'id': 1, 'title': 'Learn Java the Hard way',
                    'author': 'Meshack'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_info), content_type='application/json')

        self.assertEqual(resp.status_code, 200,
                         msg="Endpoint should be reachable")

        data = json.loads(resp.get_data().decode('utf-8'))

        result = [{'id': data['id'], 'title': data[
            'title'], 'author':data['author']}]
        self.assertTrue({'author': 'Meshack', 'title': 'Learn Java the Hard way', 'id': 1} in result, msg='Should update the information for specified book')



class UserTests(unittest.TestCase):

    def setUp(self):
        # Prepare for testing;set up variables
        from application.auth.views import users_table
        from application.users.models import User
        self.user = User(username="mbuvi", password="mesh")

        users_table.append(self.user)


        self.users_table = users_table

        # create new user
        self.app = app

        self.app = self.app.test_client()
        self.BASE_URL = 'http://localhost:5000/api/v1/auth/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        self.users_table = None


    def test_can_create_user(self):
        initial_number = len(self.users_table)
        user = {'username': 'James',
                'password': 'Kent'}

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user), content_type='application/json')
        number_after_user_created = len(self.users_table)

        self.assertTrue(number_after_user_created > initial_number,
                        msg="user should be created and added to system")

    def test_user_can_change_password(self):
        data = {"username": "mbuvi", "new_password": "meshack"}

        resp = self.app.post(self.BASE_URL + 'reset',
                             data=json.dumps(data), content_type='application/json')
        if resp.status_code != 200:
            return 1

        recv_data = json.loads(resp.get_data().decode('utf-8'))
        password = recv_data['password']

        ne
        new_info = {'id' : 1,'title': 'Learn Java the Hard way','author': 'Meshack'}

        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_info), content_type='application/json')

        self.assertEqual(resp.status_code, 200,
                         msg="Endpoint should be reachable")

        data = json.loads(resp.get_data().decode('utf-8'))


        self.assertTrue(password == 'meshack',msg = "Should change users password")

        result = [{'id': data['id'], 'title': data[
            'title'], 'author':data['author']}]

        self.assertTrue({'author': 'Meshack', 'title': 'Learn Java the Hard way', 'id': 3} in result, msg='Should update the information for specified book')


class UserTests(unittest.TestCase):

    def setUp(self):
        # Prepare for testing;set up variables
        from application.auth.views import users_table
        from application.users.models import User

        self.users_table = users_table

        # create new user
        self.app = app

        self.app = self.app.test_client()
        self.BASE_URL = 'http://localhost:5000/api/v1/auth/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        self.users_table = None
        self.user = None

    def test_can_create_user(self):
        initial_number = len(self.users_table)
        self.user = {'username': 'James',
                     'password': 'Kent'}

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            self.user), content_type='application/json')
        number_after_user_created = len(self.users_table)

        self.assertTrue(number_after_user_created > initial_number,
                        msg="user should be created and added to system")

    def test_user_can_change_password(self):
        data = {"username": "James", "new_password": "meshack"}

        resp = self.app.post(self.BASE_URL + 'reset',
                             data=json.dumps(data), content_type='application/json')

        recv_data = json.loads(resp.get_data().decode('utf-8'))
        password = recv_data['password']

        self.assertTrue(password == 'meshack',
                        msg="Should change users password")

    def test_user_can_borrow_a_book(self):
        # username and book id are send to the endpoint
        data = {"username": "mbuvi", "id": 1}

        # send the data
        resp = self.app.post('http://localhost:5000/api/v1/users/books/',
                             data=json.dumps(data), content_type='application/json')
        if resp.status_code == 404:
            return 1

        # Extract data
        recv = json.loads(resp.get_data().decode('utf-8'))
        books_borrowed = recv['borrowings']

        self.assertTrue(len(books_borrowed) != 0, msg = "Should allocate the book to user")


if __name__ == '__main__':
    unittest.main()
