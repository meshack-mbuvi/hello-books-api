from application import db
from application.models.bookmodels import Rentals as rentals


class Author(db.Model):
    __tablename__ = 'author'

    author_id = db.Column(db.Integer, primary_key=True)
    author_data = db.Column(db.String(50), nullable=False)
    books_authored = db.Column(db.Integer, nullable=False)

    books = db.relationship('Book', backref='author', lazy=True)

    def __init__(self, details):
        self.author_data = details
        self.books_authored = 0

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    secondname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    books = db.relationship('Rentals')

    def __init__(self, firstname, secondname, username, email, password):
        self.firstname = firstname
        self.secondname = secondname
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()


class Admin(User):

    def __init__(self, firstname, secondname, username, email, password):
        super().__init__(firstname, secondname, username, email, password)
        self.admin = True

    def save(self):
        super().save()
