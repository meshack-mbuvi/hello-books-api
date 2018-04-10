from flask import request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from . import blacklist, users_table
from ..models.usermodel import *

'''prepare seeds for the project'''
# An admin
hashed_password = generate_password_hash('meshack', method='sha256')
user = Admin('mbuvi', password=hashed_password)
users_table[len(users_table) + 1] = user

# A normal user
hashed_password = generate_password_hash('meshack', method='sha256')
user = User('mbuv', password=hashed_password)
users_table[len(users_table) + 1] = user


class Register(Resource):

    def post(self):
        """ Create new user account.
        User provides username and password which we confirm before creating an account
        :return: Either user created successfully, missing fields or username taken
        """
        data = request.get_json()

        if 'username' not in data or 'password' not in data:
            return {"Message": "username and password must be provided"}, 400
        username = data['username']
        password = data["password"]

        if len(username) < 1 or len(password) < 8:
            return {"Message": "username cannot be empty and password must be over 8 characters long"}, 400
        # Retrieve existing users
        users = users_table.values()

        user_exists = [user for user in users if user.username == username]

        if user_exists:
            return {"Message": "Username already taken, choose a new one"}, 409

        hashed_password = generate_password_hash(
            password, method='sha256')

        # create an admin if admin is set or a normal user
        if 'admin' in data:
            users_table[len(users_table) + 1] = Admin(username, password=hashed_password)

        else:
            users_table[len(users_table) + 1] = User(username, password=hashed_password)
        return ({'message': 'Account added successfully'}), 201


class Reset(Resource):
    def put(self):
        """Modify user password
        User provides new password and must be logged in.
        We confirm where use is genuine and then update the password.
        """
        data = request.get_json()
        # get existing users
        users = users_table.values()

        if 'username' not in data or 'password' not in data:
            return {"Message": "Make sure you fill all required fields"}, 400

        for user in users:
            if user.username == data['username']:
                hashed_password = generate_password_hash(
                    data['password'], method='sha256')

                user.password = hashed_password

                return {'message': 'Password changed successfully'}, 200

            else:
                return {'message': 'Either original password or username is wrong'}, 404


class Login(Resource):
    """This is an endpoint resource for signing users in our api"""

    def post(self):
        """Sign in a given user
        Compares the provided username and password with those already saved in the system.
        If user is genuine, we return a token to be used by user on subsequent queries.
        """
        data = request.get_json()
        if 'username' in data or 'password' in data:
            username = data['username']
            users = users_table.values()
            for user in users:
                if user.username == username and \
                        check_password_hash(user.password, data['password']):
                    token = create_access_token(identity=username)
                    return ({'token': token}), 200

            return make_response('Sorry, we could not verify you.Use correct details and try again', 401)

        else:
            return make_response('username and password must be provided.', 401)


class Logout(Resource):
    @jwt_required
    def post(self):
        """Log out a given user by blacklisting user's token
        """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return ({'message': "Successfully logged out"}), 200
