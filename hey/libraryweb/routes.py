
from flask import render_template, flash, redirect, url_for, abort, request
from flask.templating import render_template_string
from wtforms.validators import data_required, url
from libraryweb.models import User, Book, Borrow
from libraryweb.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdateBookForm, RequestResetForm, ResetPasswordForm
from libraryweb import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from flask_mail import Message



@app.route('/home')
def home():
    page = request.args.get('page',1, type=int)
    books = Book.query.order_by(Book.date_added.desc()).paginate(per_page=5,page=page)
    return render_template('home.html', title='home', header = 'Home', books = books,page=page)

@app.route('/book/<int:book_id>')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title='book', book=book, header=book.name)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if current_user.role != 'librarian':
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('This book has been deleted','warning')
    return redirect(url_for('home'))

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
            form.book.data = ""
            form.author.data=""
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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='graciezzztest@gmail.com', recipients = [user.email])
    msg.body=f''' <h3>To reset your password, visit the followin link:</h1>
<b>{url_for('reset_token', token =token, _external=True)}</b>    
    '''
    msg.html = msg.body
    mail.send(msg)
    


@app.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent to {form.email.data}','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset PAssword', form =form)


@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Expired/invalid token !','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated !', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='reset password', form = form)
