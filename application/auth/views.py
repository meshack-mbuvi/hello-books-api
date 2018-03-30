
from flask_restful import Resource
from flask import request

from application.users.usermodel import User
from application import users_table


class Register(Resource):
    # Generates new id for a given user

    def getuserId(self):
        if len(users_table) == 0:
            return 0
        return len(users_table) + 1
    # This resource creates a new user account

    def post(self):
        # create new user here

        if 'username' not in request.json or 'password' not in request.json:
            return {"Message": "Fill all fields and try again"}, 201

        # confirm no user with this username exists in our system
        username = request.json['username']

        if(len(users_table) != 0):
            for key in users_table:
                if users_table[key]['username'] == username:
                    return {"Message": "The username is already taken"}

        password = request.json['password']

        user = User(username, password)

        user_id = self.getuserId()

        users_table[user_id] = user.getdetails()

        return {'user details': user.getdetails()}, 201


class Reset(Resource):

    def post(self):
        # Confirm the right fields are filled before proceeding
        if 'username' not in request.json or 'new_password' not in request.json:
            return {"Message": "Make sure to fill all required fields"}

        # we are sure everything is ready at this point
        username = request.json['username']
        password = request.json['new_password']

        # Get the user with given username
        for key in users_table:
            if users_table[key]['username'] == username:
                # set the new password now
                users_table[key]['pasword'] = password

                return users_table[key], 201

            else:
                return {'Message': 'No user found with that username'}, 301
