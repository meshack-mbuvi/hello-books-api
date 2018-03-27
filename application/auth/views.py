
from flask_restful import Resource
from flask import request

from application.users.models import User

# A list for holding users
users_table = []

class Reset(Resource):
	def post(self):
		# Confirm the right fields are filled 
		if 'username' not in request.json or 'new_password' not in request.json:
			return {"Message":"Make sure to fill all required fields"}

		username = request.json['username']
		password = request.json['new_password']
		# Get the user with given username
		user = [user for user in users_table if user.username == username]
		if not user:
			return {"Message":"No user found with that username"}

		users_table.remove(user[0])
		user[0].password = password
		users_table.append(user[0])

return {"username":user[0].username,"password":user[0].password}
