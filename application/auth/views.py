
from flask_restful import Resource
from flask import request, jsonify, session
import jwt
import datetime

from application.users.usermodel import User
from application import users_table

JWT_ALGORITHM = 'HS256'
JWT_SECRET = 'we are secretive'

def login_method(username):
    session['username'] = username
    return True

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
        if 'username' not in request.json or 'new_password' not in request.json or not request.json:
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


class Login(Resource):

    def post(self):
        # confirm all field are field and the right format is used
        if not request.json or 'username' not in request.json or 'password' not in request.json:
            return {'message': 'Ensure you fill all fields and you use json format in your requests.'}

        # extract the username and password for the user
        username = request.json['username']
        password = request.json['password']

        # check for user in our users_table
        for key in users_table:
            if users_table[key]['username'] == username and users_table[key]['password'] == password:
                # login the user here
                auth = request.authorization

                payload = {
                        'username': username, 'exp': datetime.datetime.utcnow() 
                            + datetime.timedelta(minutes=1)
                    }
                token = jwt.encode(payload,JWT_SECRET, JWT_ALGORITHM)

                login_method(username)
                print(session)
                print(session['username'], "Yes")

                return jsonify({'message': 'user logged in successfully'})

            else:
                return jsonify({'message': 'User not logged in'})
