
from flask_restful import Resource
from flask import request, jsonify, make_response
import datetime

from application.users.usermodel import User
from application import users_table
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps


# Wrapper function for checking user tokens
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # declare variable to hold current user
        current_user = None

        # Token is present
        try:
            # Decode the token
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # get the username from the decoded data and query the users_table
            # for the username
            username = data['username']
            for key in users_table:
                if (users_table[key]['username'] == username):
                    current_user = username
        except:

            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


class Register(Resource):
    # Generates new id for a given user

    def getuserId(self):
        if len(users_table) == 0:
            return 0
        return len(users_table) + 1
    # This resource creates a new user account

    def post(self):
        # create new user here
        data = request.get_json()

        # check tha all fields are filled before proceding
        if not data['username'] or not data['password']:
            return make_response({"Message": "Fill all fields and try again"}, 400)

        # get username from the received data
        username = data['username']


        # confirm no user with that username exists before creating new one
        # checking the size of users_table tells whether this is the first user
        # in our api
        if(len(users_table) != 0):
            for key in users_table:
                if users_table[key]['username'] == username:

                    print(new_user.getdetails())
                    return {"Message": "The username is already taken"}

        # We can create a new user with given username now
        # Hash password before saving it
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        new_user = User(username, password=hashed_password, admin=False)

        # Get the user_id and add new_user to users_table
        user_id = self.getuserId()
        users_table[user_id] = new_user.getdetails()

        return {'user details': new_user.getdetails()}, 201


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
                return {'Message': 'No user found with that username'}, 404


class Login(Resource):

    def post(self):

        # get the authorization headers
        auth = request.authorization

        # check that auth is set and/or username and password fields are filled
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = {}

        # find the user from users_table with matching username
        for key in users_table:
            if users_table[key]['username'] == auth.username:
                user = users_table[key]

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'username': user['username'],
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                               app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('UTF-8')})

        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


class Logout(Resource):

    def post(self):
        if not request.json or 'username' not in request.json:
            return {'message': 'Ensure you fill all fields and use json format'}

        username = request.json['username']
        try:
            # check that username is set in the sesson object and reset it
            if session['username'] == username:
                session['username'] = None
                return {'message': 'Logged out successfully'}, 200
        except Exception as e:
            return {'message': 'not logged in'}
