from application import db
from datetime import datetime, timedelta

class Rentals(db.Model):
    __tablename__ = 'rentals'


# rentals = db.Table('rentals',
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column('isbn', db.String(30), db.ForeignKey('books.isbn'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'))
    rental_date = db.Column('rental_date', db.DateTime, nullable=False, default=datetime.utcnow())
    due_date = db.Column('due_date', db.DateTime, nullable=False, default=(datetime.utcnow() + timedelta(days=1)))
    returned = db.Column('returned', db.Boolean, nullable=False, default=False)
    books = db.relationship('Book')

    def __init__(self):
        self.rental_date = datetime.utcnow()
        self.due_date = datetime.utcnow() + timedelta(days=1)


class BookCategory(db.Model):
    __tablename__ = 'bookcategories'
    cat_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, index=True, nullable=False)
    copies = db.Column(db.Integer, nullable=False)

    # Relationship for books and category; one can access category from Book class using Book.category
    books = db.relationship('Book', backref='category', lazy=True)

    def __init__(self, title):
        self.title = title
        self.copies = 0

    def save(self):
        db.session.add(self)
        db.session.commit()


class Book(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.String(30), primary_key=True, unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))
    cat_id = db.Column(db.Integer, db.ForeignKey('bookcategories.cat_id'))
    available = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, isbn):
        self.isbn = isbn
        self.available = True

    def save(self):
        db.session.add(self)
        db.session.commit()
