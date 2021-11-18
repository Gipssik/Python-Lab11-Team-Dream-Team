from flask import render_template, url_for, flash, redirect
from flask_login import login_user

from . import app, bcrypt, db
from .forms import RegistrationForm, LoginForm
from .models import User, Group, Album


@app.route('/home', methods=['GET'])
def home():
    musicians = Group.query.all()
    return render_template('home.html', title='Головна', musicians=musicians)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Аккаунт успішно створено!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Реєстрація', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        flash('Невдача. Перевірте логін і пароль.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/groups/create', methods=['GET', 'POST'])
def create_group():
    # form = None
    # if form.validate_on_submit():
    #     group = Group(
    #         name=form.name.data,
    #         content=form.content.data,
    #         data_created=form.content_data.data,
    #         image=form.image.data
    #     )
    #
    #     for username in form.users.data:
    #         user = User.query.filter_by(username=username).first()
    #         if not user:
    #             flash('Користувача не знайдено', 'danger')
    #             return redirect(url_for('create_group'))
    #         user.group = group
    #
    #     db.session.add(group)
    #     db.session.commit()
    #     flash('Групу успішно створено!', 'success')
    #     return redirect(url_for('home'))
    # return render_template('create_group.html', title='Create Group', form=form)
    ...


@app.route('/groups/<int:group_id>')
def group_page(group_id):
    group = Group.query.get(group_id)
    albums = Album.query.filter_by(group=group).all()
    return render_template('group_page.html', title=group.name, albums=albums)
