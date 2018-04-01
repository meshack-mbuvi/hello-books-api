from run import *
import unittest
import json

class UserTests(unittest.TestCase):

    def setUp(self):
        # Prepare for testing;set up variables

        self.user = User(username="mbuvi", password="mesh")

        users_table[len(users_table) + 1] = self.user.getdetails()

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
        user = {'username': 'Jacob',
                'password': 'munyasya'}

        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            user), content_type='application/json')

        # number of users after adding a new user
        number_after_user_created = len(self.users_table)

        # new number of users should be greater than the original one
        self.assertTrue(number_after_user_created > initial_number,
                        msg="user should be created and added to system")

    def test_user_can_change_password(self):
        data = {"username": "mbuvi", "new_password": "meshack"}
        # get username from the users_table
        initial_password = None
        for key in users_table:
            if users_table[key]['username'] == data['username']:
                user = users_table[key]
                try:
                    initial_password = user['password']
                    
                except Exception as e:
                    return 'user does not exist',404


        # Change the password and confirm that is has changed
        resp = self.app.post(self.BASE_URL + 'reset',
                             data=json.dumps(data), content_type='application/json')
        if resp.status_code != 200:
            return 1

        recv_data = json.loads(resp.get_data().decode('utf-8'))
        # Get the new password
        password = recv_data['password']

        self.assertEqual(resp.status_code, 200,
                         msg="Endpoint should be reachable")

        self.assertTrue(initial_password != password,
                        msg="Should change users password")




if __name__ == '__main__':
    unittest.main()
