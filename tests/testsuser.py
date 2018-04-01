from base64 import b64encode
from run import *
import unittest
import json


class UserTests(unittest.TestCase):

    def setUp(self):
        # Prepare for testing;set up variables

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
        # number of users before adding a new user
        initial_number = len(self.users_table)
        user = {'username': 'James',
                'password': 'Kent'}

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user), content_type='application/json')

        # number of users after adding a new user
        number_after_user_created = len(self.users_table)

        # new number of users should be greater than the original one
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

        self.assertEqual(resp.status_code, 200,
                         msg="Endpoint should be reachable")

        self.assertTrue(password == 'meshack',
                        msg="Should change users password")

    def test_user_can_login(self):
        # username and password  for the user
        user_data = {'username': 'James', 'password': 'Kent'}

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




if __name__ == '__main__':
    unittest.main()
