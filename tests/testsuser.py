from base64 import b64encode
from run import *
import unittest
import json
from instance.config import configuration
from application.views import users_table


class UserTests(unittest.TestCase):

    def setUp(self):
        """Prepares variables to be used by test methods"""

        self.users_table = users_table

        # create new user
        self.app = app
        self.app.config.from_object(configuration['testing'])

        self.app = self.app.test_client()
        self.BASE_URL = '/api/v1/auth/'

    def tearDown(self):
        """Clean our environment before leaving"""
        self.app = None
        self.BASE_URL = None
        self.users_table = None

    def test_can_create_user(self):
        """ Test can register new user
        This method tests that a new user can create an account.
        It compares the initial and new number of the users after creating a new user.
        The new number of users should be greater than the initial one.
        """
        initial_number = len(users_table)
        user_data = {'username': 'Jacob', 'password': 'munyasya'}
        self.app.post(self.BASE_URL + 'register', data=json.dumps(user_data), content_type='application/json')
        new_number = len(users_table)
        self.assertTrue(new_number > initial_number, msg="user account should be created.")

    def test_existing_user_cannot_create_account(self):
        """Test existing user cannot create an account
        This method checks that number of users before and after creating new user is the same.
        The system has a user with username mbuvi"""
        initial_number = len(self.users_table)
        user_data = {'username': 'mbuvi', 'password': 'meshack'}
        self.app.post(self.BASE_URL + 'register', data=json.dumps(user_data), content_type='application/json')
        number_after_user_created = len(self.users_table)
        self.assertTrue(number_after_user_created == initial_number, msg="Should not register user account")

    def test_cannot_create_account_with_empty_fields(self):
        """ Test username and password must be provided when creating account
        compare the size before and after creating new user with empty fields"""
        initial_number = len(self.users_table)
        user_data = {'username': '', 'password': ''}
        self.app.post(self.BASE_URL + 'register', data=json.dumps(user_data), content_type='application/json')
        number_after_user_created = len(self.users_table)
        self.assertTrue(number_after_user_created == initial_number, msg="user should be created and added to system")

    def test_user_can_change_password(self):
        """Test user can change account password
        It checks for message returned.
        """
        user_data = {"username": 'mbuvi', "password": 'meshack', "new_password": "munyasya1"}
        response = self.app.put(self.BASE_URL + 'reset', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['message'], 'Password changed successfully', msg="Should change users password")

    def test_cannot_change_password_for_non_existing_user(self):
        """Test cannot change password for non-existing user
        checks the message returned from the endpoint showing that user does not exist
        """
        user_data = {"username": 'dfhsldkghsdkjkljil', "password": "passs", "new_password": "meshsf"}
        response = self.app.put(self.BASE_URL + 'reset', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 404, msg="Endpoint should be reachable")
        self.assertEqual(received_data['message'], 'Either original password or username is wrong',
                         msg="Cannot change password for non-existence user")

    def test_user_can_login(self):
        """Test that a genuine user can login
        After successful login, the endpoint should return an authorization token
        """
        user_data = {'username': 'mbuvi', 'password': 'meshack'}
        response = self.app.post(self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertTrue(received_data['token'], msg="User should be logged in")

    def test_login_with_wrong_details_fail(self):
        """Test that only valid users with correct details can login"""
        user_data = {'username': 'Jameszxcbzxfb', 'password': 'Kentzvzzbv'}
        response = self.app.get(self.BASE_URL + 'login/', data=json.dumps(user_data), content_type='application/json')
        message = response.get_data().decode('utf-8')
        self.assertTrue(message, msg="Invalid details used")

    def test_login_with_empty_details_fail(self):
        """Test that user cannot log in by using empty fields"""
        user_data = {'username': '', 'password': ''}
        response = self.app.get(self.BASE_URL + 'login/', data=json.dumps(user_data), content_type='application/json')
        message = response.get_data().decode('utf-8')
        self.assertTrue(message, msg="Invalid details used")

    def test_user_can_logout(self):
        """Tests whether a logged in user can log out
        User provides an authentication token"""
        user_data = {'username': 'mbuvi', 'password': 'meshack'}
        response = self.app.post(self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        token = received_data['token']
        # logout
        response = self.app.post(self.BASE_URL + 'logout', headers={'content_type': 'application/json',
                                                                    'Authorization': 'Bearer {}'.format(token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['message'], "Successfully logged out", msg="User should be logged out")


if __name__ == '__main__':
    unittest.main()
