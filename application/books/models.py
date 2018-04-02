class Book(object):

    def __init__(self, title, author):
        self.author = author
        self.title = title
        self.available = True

    def getdetails(self):
        return ({'title': self.title, 'author': self.author, 'available': self.available})
