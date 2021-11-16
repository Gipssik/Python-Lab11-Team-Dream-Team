from flask import render_template, url_for, flash, redirect

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
    #     user = User(username=form.username.data, enail=form.email.data, password=hashed_password)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('Аккаунт успішно створено!', 'success')
    #     return redirect(url_for('login'))
    # return render_template('register.html', title='Реєстрація', form=form)
    ...
