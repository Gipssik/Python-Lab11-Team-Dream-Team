from flask import render_template, url_for, flash, redirect
from flask_login import login_user, logout_user

from . import app, bcrypt, db
from .forms import RegistrationForm, LoginForm
from .models import User, Group, Album, Song


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
    return render_template('login.html', title='Логін', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

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
    #     for username in form.users.data.split(", "):
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
    # return render_template('create_group.html', title='Створення Групи', form=form)
    ...


@app.route('/groups/<int:group_id>')
def group_page(group_id):
    group = Group.query.get(group_id)
    if not group:
        flash('Група не знайдена', 'danger')
        return redirect(url_for('home'))

    albums = Album.query.filter_by(group=group).all()
    return render_template('group_page.html', title=group.name, albums=albums)


@app.route('/groups/<int:group_id>/albums/create', methods=['GET', 'POST'])
def create_album(group_id):
    # form = None
    # if form.validate_on_submit():
    #     group = Group.query.get(group_id)
    #     if not group:
    #         flash('Група не знайдена', 'danger')
    #         return redirect(url_for('create_album'))
    #
    #     album = Album(
    #         label=form.label.data,
    #         image=form.image.data,
    #         group=group
    #     )
    #
    #     db.session.add(album)
    #     db.session.commit()
    #     flash('Альбом успішно створено!', 'success')
    #     return redirect(url_for('home'))
    # return render_template('create_album.html', title='Створення Альбому', form=form)
    ...


@app.route('/groups/<int:group_id>/albums/<int:album_id>', methods=['GET', 'POST'])
def album_page(group_id, album_id):
    album = Album.query.filter_by(id=album_id, group_id=group_id).first()
    if not album:
        flash('Альбом не знайдено', 'danger')
        return redirect(url_for('home'))

    songs = Album.query.filter_by(album=album).all()
    return render_template('album_page.html', title=album.name, image=album.image, songs=songs)


@app.route('/groups/<int:group_id>/albums/<int:album_id>/edit', methods=['GET', 'POST'])
def edit(group_id, album_id):
    # form = None
    # if form.validate_on_submit():
    #     album = Album.query.filter_by(id=album_id, group_id=group_id).first()
    #     if not album:
    #         flash('Альбом не знайдено', 'danger')
    #         return redirect(url_for('home'))

    #     album.image = form.image.data
    #     album.label = form.label.data
    #
    #     song = Song(
    #         title=form.title.data,
    #         album=album,
    #         media=form.media.data
    #     )
    #
    #     db.session.add(song)
    #     db.session.commit()
    #     flash(f'Пісня успішно додана до альбому {album.label}!', 'success')
    #     return redirect(url_for('edit'))
    # return render_template('edit.html', title='Редагування', form=form)
    ...
