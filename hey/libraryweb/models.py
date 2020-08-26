from datetime import datetime, timedelta
from libraryweb import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    borrow = db.relationship('Borrow', backref='user', lazy=True)

    def __repr__(self):
        return f'User: {self.username},{self.email},{self.id}'


class Book(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    author = db.Column(db.String(200), unique=False, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    image_file = db.Column(db.String(50), nullable=False,
                           default='default_book.jpg')
    borrow = db.relationship('Borrow', backref='book', lazy=True)

    def __repr__(self):
        return f'Book: {self.name},{self.author},{self.id}'


class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('book.id'),nullable=True)
    time_borrowed = db.Column(db.DateTime, default=datetime.utcnow,nullable=True)
    time_due = db.Column(db.DateTime, default=datetime.utcnow()+timedelta(days = 30),nullable=True)

    def __repr__(self):
        return f'Person number {self.user_id} has borrowered {self.book_id}'