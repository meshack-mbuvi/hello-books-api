from flask import request, make_response
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token
from flask_restful import Resource
from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash

from . import blacklist
from ..models.usermodel import *


class Register(Resource):
    """Handles user account registration.

    """

    def data_valid(self, data):
        """ checks whether data is a valid string

        :param data:
        :return: True for string data, False otherwise.

        """
        result = [c for c in data if c.isnumeric() or c.isspace() or c.isdigit() ]
        if len(result) == 0 and len(data) > 0:
            return True
        return False

    def post(self):
        """ Creates new user account.
        User provides username and password which we confirm before creating an account
        checks whether a user with given username exists in the database before creating the user account.
        :return: dictionary with message and status code depending on valid of data and request success.

        """
        data = request.get_json()

        if 'username' not in data or 'password' not in data:
            return {"Message": "username and password must be provided"}, 400
        username = data['username']
        firstname = data['firstname']
        secondname = data['secondname']
        email = data['email']
        password = data["password"]

        if not validate_email(email) or len(password) < 8:
            return {"Message": "Either email is invalid and password is less than 8 characters long"}, 400

        if not self.data_valid(firstname) or not self.data_valid(secondname):
            return {'Message': 'firstname or secondname cannot contain digits or spaces'}, 400
        # Retrieve existing users
        user = db.session.query(User).filter(User.username == username).first()

        if user:
            return {"Message": "Username already taken, choose a new one"}, 409

        hashed_password = generate_password_hash(
            password, method='sha256')

        # create an admin if admin is set or a normal user
        if 'admin' in data:
            user = Admin(firstname, secondname, username, email, password=hashed_password)
            user.save()

        else:
            user = User(firstname, secondname, username, email, password=hashed_password)
            user.save()
        return ({'message': 'Account added successfully'}), 201


class Reset(Resource):
    def put(self):
        """Modify user password
        User provides new password and must be logged in.
        We confirm where use is genuine and then update the password.

        :return message and status code for request execution.

        """
        data = request.get_json()
        if 'username' not in data or 'password' not in data or 'new_password' not in data:
            return {"Message": "All required fields must be filled and"
                               " username should not contain spaces or numbers"}, 400

        username = data['username']
        # identify user
        user = db.session.query(User).filter(User.username == username).first()

        if user is None:
            return {'message': 'user with given username is not found'}, 404

        if user.username == data['username'] and check_password_hash(user.password, data['password']):
            hashed_password = generate_password_hash(
                data['new_password'], method='sha256')

            user.password = hashed_password
            db.session.commit()
            return {'message': 'Password changed successfully'}, 200

        else:
            return {'message': 'Either original password or username is wrong'}, 403


class Login(Resource):
    """Handles user authentication."""

    def post(self):
        """Sign in a given user
        Compares the provided username and password with those already saved in the system.
        If user is genuine, we return a token to be used by user on subsequent queries.
        :arg
            request object with username and password.
        :return token if user is authenticated or message and status code otherwise.

        """
        data = request.get_json()
        if 'username' in data or 'password' in data:
            username = data['username']
            user = db.session.query(User).filter(User.username == username).first()
            # confirm user exists
            if user is not None:
                if check_password_hash(user.password, data['password']):
                    token = create_access_token(identity=username)
                    return ({'token': token}), 200

                return make_response('Sorry, we could not verify you.Use correct details and try again', 401)
            else:
                return {'message': 'User does not exist'}, 404

        else:
            return make_response('username and password must be provided.', 401)


class Logout(Resource):
    """handles user logout."""
    @jwt_required
    def post(self):
        """Log out a given user by blacklisting user's token
        :return
            message and status code.
        """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return ({'message': "Successfully logged out"}), 200
