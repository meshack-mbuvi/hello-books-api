
from flask_restful import Resource
from flask import request, jsonify, make_response
import datetime

from application.users.usermodel import User
from application import app, blacklist
from application import users_table
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)

'''populate users_table'''
hashed_password = generate_password_hash('meshack', method='sha256')
new_user = User('mbuvi', password=hashed_password, admin=False)
# save user details to user_tableusers_table[len(users_table)] =
# new_user.getdetails()


hashed_password = generate_password_hash('macks', method='sha256')
new_user = User('mercy', password=hashed_password, admin=False)

users_table[len(users_table)] = new_user.getdetails()

hashed_password = generate_password_hash('kavas', method='sha256')
new_user = User('Gladys', password=hashed_password, admin=False)

users_table[len(users_table)] = new_user.getdetails()


class Register(Resource):
    
    def post(self):
        # create new user here
        data = request.get_json()

        # check tha all fields are filled before proceding
        if not data['username'] or not data['password']:
            return {"Message": "Fill all fields and try again"}, 400

        # confirm no user with that username exists before creating new one
        # checking the size of users_table tells whether this is the first user
        # in our api
        # get username from the received data
        username = data['username']
        for key in users_table:
            if users_table[key]['username'] == username:

                return {"Message": "The username is already taken"}, 409

            else:
                # We can create a new user with given username now
                # Hash password before saving it
                hashed_password = generate_password_hash(
                    data['password'], method='sha256')
                new_user = User(
                    username, password=hashed_password, admin=False)
                # Get the user_id and add new_user to users_table
                # save user details to user_table
                users_table[len(users_table) + 1] = new_user.getdetails()
                return {'user details': new_user.getdetails()}, 201


class Reset(Resource):

    def post(self):
        # Confirm the right fields are filled before proceeding
        data = request.get_json()
        if not data['username'] or not data['new_password'] or not data['password']:
            return make_response({"Message": "Make sure to fill all required fields"}, 400)

        # we are sure everything is ready at this point
        username = data['username']
        password = data['password']
        new_password = data['new_password']

        # Get the user with given username
        for key in users_table:
            if users_table[key]['username'] == username and \
            check_password_hash(users_table[key]['password'],password):

                # generate hash for new password and save update it for the
                # given user
                hashed_password = generate_password_hash(
                    data['new_password'], method='sha256')
                initial_password = users_table[key]['password']

                users_table[key]['password'] = hashed_password

                return {'initial password' : initial_password,'new password':users_table[key]['password']}, 200

            else:
                return {'Message': 'No user found with that username'}, 404


class Login(Resource):

    def get(self, headers={}):

        # get the authorization headers
        auth = request.authorization

        # check that auth is set and/or username and password fields are filled
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401)

        user = {}

        # find the user from users_table with matching username
        for key in users_table:
            if users_table[key]['username'] == auth.username:
                user = users_table[key]

        if not user:
            return make_response('Could not verify', 401)

        if check_password_hash(user['password'], auth.password):

            token = create_access_token(identity=auth.username)
            return ({'token': token}), 200

        return make_response('Invalid details used', 401)


class Logout(Resource):

    def post(self, headers={}):
        # get the authorization headers
        auth = request.authorization
        data = request.get_json()
        # check that auth is set and/or username and password fields are filled
        if not auth or not auth.username or not auth.password:
            return make_response('username and token required to continue', 401)

        user = {}

        # find the user from users_table with matching username
        for key in users_table:
            if users_table[key]['username'] == auth.username:
                user = users_table[key]

        if not user:
            return make_response('Could not verify', 401)

        # Verify user password
        if check_password_hash(user['password'], auth.password):

            # Add the token to blacklist
            blacklist.add(data['token'])

            return ({'token': 'Revoked'}), 200

        return make_response('Invalid details used', 401)
