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

        self.app = self.app.test_client()
        self.BASE_URL = '/api/v1/auth/'

        user_data = {'username': 'Jackson',
                     'password': 'munyasya'}
        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user_data), content_type='application/json')

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app = None
        self.BASE_URL = None
        self.users_table = None

    def test_can_create_user(self):
        ''' Test can create user

        This method tests that a new user can create an account.
        It compares the initial and new number of the users after creating a new user.
        The new number of users should be greater than the initial one.

        '''

        user = {'username': 'Jacob',
                'password': 'munyasya'}

        initial_number = len(users_table)

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user), content_type='application/json')

        new_number = len(users_table)
        self.assertTrue(new_number > initial_number,
                        msg="user should be created and added to system")

    def test_existing_user_cannot_create_account(self):
        # Test existing user cannot create an account
        # This method checks that number of users before and creating new user is the same.
        initial_number = len(self.users_table)
        user_data = {'username': 'mercy',
                'password': 'munyasya'}

        response = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user_data), content_type='application/json')
        
        
        number_after_user_created = len(self.users_table)
        self.assertTrue(number_after_user_created == initial_number,
                        msg="user should not be created and added to system")

    def test_cannot_create_account_with_empty_fields(self):
        # Test username and password must be provided when creating account
        # compare the size before and after creating new user with empty fields
        initial_number = len(self.users_table)
        user = {'username': '',
                'password': ''}

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user), content_type='application/json')
        number_after_user_created = len(self.users_table)
        self.assertTrue(number_after_user_created == initial_number,
                        msg="user should be created and added to system")

    def test_user_can_change_password(self):
        '''Test user can change account password
        compare the initial and new password to see whether they are the same
        '''

        user_data = {"username": 'mercy', "password": 'macks',
                     "new_password": "munyasya1"}
        response = self.app.post(self.BASE_URL + 'reset',
                                 data=json.dumps(user_data), content_type='application/json')

        received_data = json.loads(response.get_data().decode('utf-8'))
       
        initial_password = received_data['initial password']
        new_password = received_data['new password']

        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should be reachable")

        self.assertNotEqual(initial_password, new_password,
                            msg="Should change users password")

    def test_cannot_change_password_for_non_existing_user(self):
        '''Test cannot change password for non-existing user
        checks the message returned from the endpoint showing that user does not exist
        '''
        user_data = {"username": 'dfhsldkghsdkjkljil',
                "password": "passs", "new_password": "meshsf"}

        response = self.app.post(self.BASE_URL + 'reset',
                             data=json.dumps(user_data), content_type='application/json')

       
        received_data = json.loads(response.get_data().decode('utf-8'))
        message = received_data['Message']

        self.assertEqual(response.status_code, 404,
                         msg="Endpoint should be reachable")

        self.assertEqual(message, 'No user found with that username',
                         msg="Cannot change password for non-existence user")

    def test_user_can_login(self):
        ''' Test that a genuine user can login
        '''
        user_data = {'username': 'Jacob', 'password': 'munyasya'}

        headers = {}
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] + ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        response = self.app.get(
            self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json', headers=headers)

        received_data = json.loads(response.get_data().decode('utf-8'))

        # Test for message received.
        self.assertTrue(received_data[
            'token'], msg="User should be logged in")

    def test_login_with_wrong_details_fail(self):
        '''Test that only valid users with correct details can login'''
        user_data = {'username': 'Jameszxcbzxfb', 'password': 'Kentzvzzbv'}

        headers = {}
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] + ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        response = self.app.get(
            self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json', headers=headers)

        message = response.get_data().decode('utf-8')

        # Test for message received.
        self.assertTrue(message, msg="Invalid details used")

    def test_login_with_empty_details_fail(self):
        '''Test that user cannot log in by using empty fields'''
        user_data = {'username': '', 'password': ''}

        headers = {}
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] + ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        response = self.app.get(
            self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json', headers=headers)

        message = response.get_data().decode('utf-8')

        self.assertTrue(message, msg="Invalid details used")

    def test_user_can_logout(self):
        # username and password  for the user
        user_data = {'username': 'Jacob',
                     'password': 'munyasya'}

        # log in first to get a token
        headers = {}
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] + ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        # connect to the endpoint for login
        response = self.app.get(
            self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json', headers=headers)

        received_data = json.loads(response.get_data().decode('utf-8'))
        user_data['token'] = received_data['token']
        # print(user_data)

        # Then use the resulting token to log out.
        headers['Authorization'] = 'Basic ' + b64encode((user_data['username'] +
                                                         ':' + user_data['password'])
                                                        .encode('utf-8')).decode('utf-8')

        # connect to the endpoint for login
        response = self.app.post(
            self.BASE_URL + 'logout', data=json.dumps(user_data), content_type='application/json', headers=headers)

        recv_data = json.loads(response.get_data().decode('utf-8'))

        # Test for message received.
        self.assertEqual(recv_data[
            'token'], 'Revoked', msg="User should be logged out")


if __name__ == '__main__':
    unittest.main(verbosity=5)
