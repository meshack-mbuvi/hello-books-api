
class BookRentals():

    def __init__(self, username, book_id, date_borrowed, return_date):
        self.username = username
        self.book_id = book_id
        self.return_date = return_date
        self.date_borrowed = date_borrowed

    def getdetails(self): return {'username': self.username, 'book_id':
                                  self.book_id, 'date borrowed': self.date_borrowed, 'return date':
                                  self.return_date}
