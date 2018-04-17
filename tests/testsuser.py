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

    def test_can_create_an_admin(self):
        """ Tests the api can register a user who is an administrator
        checks the status code returned signifying account created successfully.
        """
        user_data = {'username': 'James', 'password': 'munyasya', 'admin': ''}
        response = self.app.post(self.BASE_URL+'register', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_cannot_create_user_without_providing_username_or_password(self):
        """ Test cannot register new user if fields for password or username are not provided
        checks for status code returned.
        """
        user_data = {'usernameasdfdghj': 'Jacob', 'passworddfghj': 'munyasya'}
        response = self.app.post(self.BASE_URL+'register', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400, msg="user account should not be created.")

    def test_cannot_create_user_with_empty_username_or_password(self):
        """ Test api cannot register new user if username is empty or password is too short
        checks for status code returned.
        """
        user_data = {'username': '', 'password': 'muny'}
        response = self.app.post(self.BASE_URL+'register', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400, msg="user account should not be created.")

    def test_existing_user_cannot_create_account(self):
        """Test existing user cannot create an account
        Checks for status code that signifies conflict in usernames"""
        user_data = {'username': 'mbuvi', 'password': 'meshackedg'}
        response = self.app.post(self.BASE_URL+'register', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 409)

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

    def test_user_cannot_change_password_if_username_or_password_is_not_provided(self):
        """Test user cannot change password if username and password fields are not provided
        Checks status code for bad request
        """
        user_data = {"usernamedsklkjhgg": 'mbuvi', "passwordhdgjh": 'meshack', "new_password": "munyasya1"}
        response = self.app.put(self.BASE_URL + 'reset', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

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
        After successful login, the endpoint should return an authorization token and a status code of 200
        """
        user_data = {'username': 'mbuvi', 'password': 'meshack'}
        response = self.app.post(self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_details_fail(self):
        """Test that only valid users with correct details can login"""
        user_data = {'username': 'Jameszxcbzxfb', 'password': 'Kentzvzzbv'}
        response = self.app.post(self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_without_providing_username_or_password_fields(self):
        """Test that without filling username or password, a user cannot log in to the api"""
        user_data = {'usernamednbang': 'Jameszxcbzxfb', 'passworddfgd': 'Kentzvzzbv'}
        response = self.app.post(self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_with_empty_details_fail(self):
        """Test that user cannot log in by using empty fields for password and username"""
        user_data = {'username': '', 'password': ''}
        response = self.app.post(self.BASE_URL + 'login', data=json.dumps(user_data), content_type='application/json')
        message = response.get_data().decode('utf-8')
        self.assertTrue(message, msg="Invalid details used")

    def test_user_can_logout(self):
        """Tests that a logged in user can log out
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
