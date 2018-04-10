class User(object):

    def __init__(self, username, password, user_id=None):
        self.username = username
        self.password = password
        self.admin = False


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.admin = True
