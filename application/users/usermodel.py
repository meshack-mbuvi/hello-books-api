class User(object):

    def __init__(self, username, password, admin=False,user_id=None):
        self.username = username
        self.password = password
        self.admin = admin

    def getdetails(self):
        return({'username': self.username, 'password': self.password, 'admin': self.admin})
