
from flask import render_template, flash, redirect, url_for
from flask.globals import request
from wtforms.validators import url
from libraryweb.models import User, Book, Borrow
from libraryweb.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdateBookForm
from libraryweb import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os


@app.route('/home')
def home():
    books = Book.query.order_by(Book.date_added.desc())
    return render_template('home.html', title='home', header = 'Home', books = books)

@app.route('/book/update', methods = ['POST','GET'])
@login_required
def book_update():
    if current_user.role == 'librarian':
        form = UpdateBookForm()
        if form.validate_on_submit():
            book = form.book.data
            author = form.author.data
            cover_pic = save_picture(form.picture.data,'book_pics')
            book = Book(name = book, author = author,image_file = cover_pic)
            db.session.add(book)
            db.session.commit()
            flash('The book has been added to the shelf','success')
        return render_template('book_update.html', title='home', librarian = True, form = form, header ='Book Update')
    else:
        flash('You are not a librarian !','danger')
        return redirect(url_for('home'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.position.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created ! You are now able to login !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Sign Up')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('welcome!', 'warning')
            return redirect(url_for('home'))
        else:
            flash('Login Unsccuessful. Please check email and password.','danger')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture, dir):
    random_hex=secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/{dir}',picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data,'user_pics')
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email = form.email.data
        current_user.role = form.position.data
        db.session.commit()
        flash('Your account has been updated !','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.position.data = current_user.role
    image_file = url_for('static', filename='user_pics/'+current_user.image_file)
    return render_template('account.html',title='account', header="Account", image_file=image_file, form=form)

@app.route('/')
def default():
    return redirect(url_for('home', header="Home"))


@app.route('/test')
def test():
    flash('Test !','info')
    return redirect(url_for('home', header="Home"))
