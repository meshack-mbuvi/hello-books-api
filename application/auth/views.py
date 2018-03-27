
from flask_restful import Resource
from flask import request

from application.users.models import User

# A list for holding users
users_table = []

class Register(Resource):
	# This resource creates a new user account
	def post(self):
		# create new user here

		user = User(username = 'meshack',password = 'password')
		users_table.append(user)

		return {'user details':{'username':user.username,'borrowings':user.borrowed_books}}


