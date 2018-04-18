import json
import unittest

from application.models.usermodel import *
from application import *


class UserTests(unittest.TestCase):

    def setUp(self):
        """Prepares variables to be used by test methods. """

        self.app = app_config('testing')
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()
        db.create_all()

    def tearDown(self):
        """Clean our environment before leaving"""
        self.app = None
        db.session.remove()
        db.drop_all()

    def test_can_create_user(self):
        """ Check number of records before creating a new user, create a user,
        then check the number of records and compare both numbers.

        """
        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        number_of_users_before = db.session.query(User).all()
        self.app.post('/api/v1/auth/register', data=json.dumps(user_data), content_type='application/json')
        number_of_users_after = db.session.query(User).all()
        self.assertTrue(number_of_users_after > number_of_users_before, msg="user account should be created.")

    def test_can_create_an_admin(self):
        """ Create an admin user account and query the database to confirm that user has been created."""

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya', 'admin': 'True'}
        response = self.app.post('/api/v1/auth/register', data=json.dumps(user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        admin_created = db.session.query(User).filter(User.username == 'Jacob').first()
        self.assertTrue(admin_created.admin)

    def test_cannot_create_user_without_providing_required_fields_like_username_or_password(self):
        """ Attempt to create a user without providing all required fields. """

        user_data = {'usernameasdfdghj': 'Jacob', 'passworddfghj': 'munyasya'}
        response = self.app.post('/api/v1/auth/register', data=json.dumps(user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400, msg="user account should not be created.")

    def test_cannot_create_user_with_empty_fields_like_username_or_password(self):
        """ Attempt to create a user with some fields having empty strings."""

        user_data = {'firstname': '', 'secondname': '', 'email': 'muasya@gmail.com', 'username': '', 'password': 'muny'}
        response = self.app.post('/api/v1/auth/register', data=json.dumps(user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400, msg="user account should not be created.")

    def test_cannot_create_user_with_digits_or_spaces_in_firstname_or_in_secondname(self):
        """ Attempt to create user with some fields having empty strings,digits or spaces."""

        user_data = {'firstname': '356d', 'secondname': '34576ydfgd', 'email': 'muasya@gmail.com', 'username': '',
                     'password': 'munyasya'}
        response = self.app.post('/api/v1/auth/register', data=json.dumps(user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400, msg="user account should not be created.")

    def test_cannot_create_user_with_invalid_email(self):
        """ Attempt to create user with an invalid email address."""

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasyagmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        response = self.app.post('/api/v1/auth/register', data=json.dumps(user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400, msg="user account should not be created.")

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
        """Attempt to create user with an already used username. """

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        self.app.post('/api/v1/auth/register', data=json.dumps(user_data), content_type='application/json')
        response = self.app.post('/api/v1/auth/register', data=json.dumps(user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_user_can_change_password(self):
        """Register a new user account and attempt to change the user password."""

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        self.app.post('/api/v1/auth/register', data=json.dumps(user_data), content_type='application/json')
        user_data = {"username": 'Jacob', "password": 'munyasya', "new_password": "munyasya1"}
        response = self.app.put('/api/v1/auth/reset', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['message'], 'Password changed successfully', msg="Should change users password")

    def test_user_cannot_change_password_if_username_or_password_is_not_provided(self):
        """After creating new user, attempt to change his password without username or password. """

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        self.app.post('/api/v1/auth/register', data=json.dumps(user_data), content_type='application/json')
        user_data = {"usernamedsklkjhgg": 'Jacob', "passwordhdgjh": 'munyasya', "new_password": "munyasya1"}
        response = self.app.put('/api/v1/auth/reset', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_cannot_change_password_for_non_existing_user(self):
        """Try to change password for non-existing user account."""

        user_data = {"username": 'dfhsldkghsdkjkljil', "password": "passs", "new_password": "meshsf"}
        response = self.app.put('/api/v1/auth/reset', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 404, msg="User not found")
        self.assertEqual(received_data['message'], 'user with given username is not found',
                         msg="Cannot change password for non-existence user")

    def test_cannot_change_password_if_password_provided_is_wrong(self):
        """Register user account and try to change password by providing username and wrong password."""

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        self.app.post('/api/v1/auth/register', data=json.dumps(user_data), content_type='application/json')

        user_data = {"username": 'Jacob', "password": "passs", "new_password": "meshsf"}
        response = self.app.put('/api/v1/auth/reset', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 403, msg="User not found")
        self.assertEqual(received_data['message'], 'Either original password or username is wrong',
                         msg="Cannot change password for non-existence user")

    def test_user_can_login(self):
        """Register a user account and try to log in using the credentials of created account. """

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        self.app.post('/api/v1/auth/register', data=json.dumps(user_data), content_type='application/json')

        user_login = {'username': 'Jacob', 'password': 'munyasya'}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertTrue(received_data['token'])

    def test_login_with_wrong_username_fail(self):
        """Create a new user account and use a different username to log the user in."""

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        self.app.post('/api/v1/auth/register', data=json.dumps(user_data), content_type='application/json')
        user_data = {'username': 'Jameszxcbzxfb', 'password': 'munyasya'}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_login_with_wrong_password_fail(self):
        """Trying login a valid username using a wrong password. """

        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        self.app.post('/api/v1/auth/register', data=json.dumps(user_data), content_type='application/json')
        user_data = {'username': 'Jacob', 'password': 'Kentzvzzbv'}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_without_providing_username_or_password_fields(self):
        """Attempt login without provifing username and password fields. """

        user_data = {'usernamednbang': 'Jameszxcbzxfb', 'passworddfgd': 'Kentzvzzbv'}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_with_empty_details_fail(self):
        """Try login with required fields all having empty values."""

        user_data = {'username': '', 'password': ''}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user_data), content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['message'], 'User does not exist')
        self.assertEqual(response.status_code, 404)

    def test_user_can_logout(self):
        """Register a new user, log him in, and then try to log him out."""

        # Register user
        user_data = {'firstname': 'Jacob', 'secondname': 'Muasya', 'email': 'muasya@gmail.com', 'username': 'Jacob',
                     'password': 'munyasya'}
        self.app.post('/api/v1/auth/register', data=json.dumps(user_data), content_type='application/json')
        # login
        user_login = {'username': 'Jacob', 'password': 'munyasya'}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user_login), content_type='application/json')

        received_data = json.loads(response.get_data().decode('utf-8'))
        token = received_data['token']
        # logout
        response = self.app.post('/api/v1/auth/logout', headers={'content_type': 'application/json',
                                                                 'Authorization': 'Bearer {}'.format(token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['message'], "Successfully logged out", msg="User should be logged out")


if __name__ == '__main__':
    unittest.main()
