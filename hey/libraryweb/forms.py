from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from libraryweb.models import User, Book
from flask_login import current_user

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Name', validators=[
                           DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm password:', validators=[
                                     DataRequired(), EqualTo('password')])
    position = SelectField('Position', choices=['teacher','student','librarian'], validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another name.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another email.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=30)])
    remember = BooleanField('remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Name', validators=[
                           DataRequired(), Length(min=2, max=20)])
    position = SelectField('Position', choices=['teacher','student'], validators=[DataRequired()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another name.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another email.')

class UpdateBookForm(FlaskForm):
    book = StringField('Book name', validators=[DataRequired()])
    author = StringField('Author(s)', validators=[DataRequired()])
    picture = FileField('Cover Picture', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Update')

    def validate_book(self, book):
        book = Book.query.filter_by(name=book.data).first()
        if book:
            raise ValidationError('That book has already been shelved !')

    