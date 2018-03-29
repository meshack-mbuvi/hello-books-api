class User(object):

	def __init__(self, username, password,admin = False ):
		self.username = username
		self.password = password
		self.admin = admin
		self.borrowed_books = []
