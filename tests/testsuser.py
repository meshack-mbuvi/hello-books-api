from base64 import b64encode
from run import *
import unittest
import json
from instance.config import configuration


class UserTests(unittest.TestCase):

    def setUp(self):
        # Prepare for testing;set up variables

        self.users_table = users_table

        # create new user
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.user = User(username="mbuvi", password="meshack")

        users_table[len(users_table) + 1] = self.user.getdetails()
        self.users_table = users_table

        self.app = self.app.test_client()
        self.BASE_URL = 'http://localhost:5000/api/v1/auth/'

        user = {'username': 'Jackson',
                'password': 'munyasya'}

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user), content_type='application/json')

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        self.users_table = None

    def test_can_create_user(self):
        # number of users before adding a new user
        initial_number = len(self.users_table)
        user = {'username': 'Jacob',
                'password': 'munyasya'}

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user), content_type='application/json')

        # number of users after adding a new user
        number_after_user_created = len(self.users_table)

        # new number of users should be greater than the original one
        self.assertTrue(number_after_user_created > initial_number,
                        msg="user should be created and added to system")

    def test_existing_user_cannot_create_account(self):
        # number of users before adding a new user
        initial_number = len(self.users_table)
        user = {'username': 'James',
                'password': 'Kent'}

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user), content_type='application/json')

        # number of users after adding a new user
        number_after_user_created = len(self.users_table)

        # new number of users should be greater than the original one
        self.assertTrue(number_after_user_created == initial_number,
                        msg="user should be created and added to system")

    def test_cannot_create_account_with_empty_fields(self):
        # number of users before adding a new user
        initial_number = len(self.users_table)
        user = {'username': '',
                'password': ''}

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user), content_type='application/json')

        # number of users after adding a new user
        number_after_user_created = len(self.users_table)

        # new number of users should be greater than the original one
        self.assertTrue(number_after_user_created == initial_number,
                        msg="user should be created and added to system")

    def test_user_can_change_password(self):

        data = {"username": "mbuvi", "password": 'mesh',
                "new_password": "munyasya1"}

        # change the password
        resp = self.app.post(self.BASE_URL + 'reset',
                             data=json.dumps(data), content_type='application/json')

        # Retrive the data
        recv_data = json.loads(resp.get_data().decode('utf-8'))
        print(recv_data)

        # Get new password
        new_pwd = recv_data['password']

        self.assertEqual(resp.status_code, 200,
                         msg="Endpoint should be reachable")

        self.assertTrue(data['password'] != new_pwd,
                        msg="Should change users password")

    def test_cannot_change_password_for_non_existend_user(self):
        data = {"username": 'dfhsldkghsdkjkljil',
                "password": "passs", "new_password": "meshsf"}

        # Get initial password
        pwd = None
        for key in users_table:
            if users_table[key]['username'] == data['username']:
                pwd = users_table[key]['password']
        # change the password
        resp = self.app.post(self.BASE_URL + 'reset',
                             data=json.dumps(data), content_type='application/json')

        # Retrive the data
        recv_data = json.loads(resp.get_data().decode('utf-8'))
        msg = recv_data['Message']

        self.assertEqual(resp.status_code, 404,
                         msg="Endpoint should be reachable")

        self.assertEqual(msg, 'No user found with that username',
                         msg="Cannot change password for non-existence user")

    def test_user_can_login(self):
        # username and password  for the user
        user_data = {'username': 'Jacob', 'password': 'munyasya'}

        headers = {}
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] + ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        # connect to the endpoint for login
        response = self.app.get(
            self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json', headers=headers)

        recv_data = json.loads(response.get_data().decode('utf-8'))

        # Test for message received.
        self.assertTrue(recv_data[
            'token'], msg="User should be logged in")

    def test_login_with_wrong_details_fail(self):
        # username and password  for the user
        user_data = {'username': 'Jameszxcbzxfb', 'password': 'Kentzvzzbv'}

        headers = {}
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] + ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        # connect to the endpoint for login
        response = self.app.get(
            self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json', headers=headers)

        msg = response.get_data().decode('utf-8')

        # Test for message received.
        self.assertTrue(msg, msg="Invalid details used")

    def test_login_with_empty_details_fail(self):
        # username and password  for the user
        user_data = {'username': '', 'password': ''}

        headers = {}
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] + ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        # connect to the endpoint for login
        response = self.app.get(
            self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json', headers=headers)

        msg = response.get_data().decode('utf-8')

        # Test for message received.
        self.assertTrue(msg, msg="Invalid details used")


if __name__ == '__main__':
    unittest.main()
