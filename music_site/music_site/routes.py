from flask import render_template, url_for, flash, redirect
from flask_login import login_user

from . import app, bcrypt, db
from .models import User


@app.route('/')
def example():
    return 'Hello world'


@app.route('/register', methods=['GET', 'POST'])
def register():
    # form = None
    # if form.validate_on_submit():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data)
    #     user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('Аккаунт успішно створено!', 'success')
    #     return redirect(url_for('login'))
    # return render_template('register.html', title='Реєстрація', form=form)
    ...


@app.route('/login', methods=['GET', 'POST'])
def login():
    # form = None
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.username.data).first()
    #     if user and bcrypt.check_password_hash(user.password, form.password):
    #         login_user(user, remember=form.remember.data)
    #         return redirect(url_for('home'))
    #     flash('Невдача. Перевірте логін і пароль.', 'danger')
    # return render_template('login.html', title='Login', form=form)
    ...
