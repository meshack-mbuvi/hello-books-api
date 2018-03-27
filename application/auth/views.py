
from flask_restful import Resource
from flask import request

from application.users.models import User

# A list for holding users
users_table = []

class Register(Resource):
    # This resource creates a new user account
    def post(self):
        # create new user here

        if 'username' not in request.json or 'password' not in request.json:
            return {"Message" : "Fill all fields and try again"},201
        # confirm no user with that username
        username = request.json['username']
        unavailable = [user for user in users_table if user.username == username]

        if unavailable:
            return {"Message" : "The username is already taken"}

        username = request.json['username']
        password = request.json['password']

        user = User(username,password)
        users_table.append(user)

        return {'user details':{'username':user.username,'borrowings':user.borrowed_books}},201
  