class Book(object):

    def __init__(self, title, author):
        self.author = author
        self.title = title
        self.user_id = None
        self.available = True