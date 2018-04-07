from flask import request, make_response, jsonify
from flask_jwt_extended import (
    create_access_token)
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from . import blacklist, users_table
from ..models.usermodel import User

'''prepare seeds for the project'''
hashed_password = generate_password_hash('meshack', method='sha256')
# save user details to user_table
user = User('mbuvi', password=hashed_password)
print(type(user))
print(user.username)
users_table.append(user)

# hashed_password = generate_password_hash('macks', method='sha256')
#
# users_table.append([User('mercy', password=hashed_password)])
#
# hashed_password = generate_password_hash('kavas', method='sha256')
#
# users_table.append([User('Gladys', password=hashed_password)])


class Register(Resource):

    def post(self):
        """ Create new user account.
        User provides username and password which we confirm before creating an account
        :return: Either user created successfully, missing fields or username taken
        """
        data = request.get_json()

        if not data['username'] or not data['password']:
            return {"Message": "Fill all fields and try again"}, 400
        username = data['username']

        user_exists = [user for user in users_table if user.username == username]

        if user_exists:
            return {"Message": "The username is already taken"}, 409
        hashed_password = generate_password_hash(
            data["password"], method='sha256')
        users_table.append(User(username, password=hashed_password))
        return {'message': 'user added successfully'}, 201


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
            if users_table[key].username == username and \
                    check_password_hash(users_table[key].password, password):

                # generate hash for new password and save update it for the
                # given user
                hashed_password = generate_password_hash(
                    data['new_password'], method='sha256')
                initial_password = users_table[key].password

                users_table[key].password = hashed_password

                return {'message': 'Password changed successfully'}, 200

            else:
                return {'message': 'either password or username is wrong'}, 404


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
            if users_table[key].username == auth.username:
                user = users_table[key]

        if not user:
            return make_response('Could not verify', 401)

        if check_password_hash(user.password, auth.password):
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
            if users_table[key].username == auth.username:
                user = users_table[key]

        if not user:
            return make_response('Could not verify', 401)

        # Verify user password
        if check_password_hash(user.password, auth.password):
            # Add the token to blacklist
            blacklist.add(data['token'])

            return ({'token': 'Revoked'}), 200

        return make_response('Invalid details used', 401)
