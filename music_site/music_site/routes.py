from flask import render_template, url_for, flash, redirect
from flask_login import login_user

from . import app, bcrypt, db
from .models import User, Group, Album, Song

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
    #     group.users = users
    #     db.session.add(group)
    #     db.session.commit()
    #     flash('Групу успішно створено!', 'success')
    #     return redirect(url_for('home'))
    # return render_template('create_group.html', title='Create Group', form=form)
    ...

@app.route('/groups/<int:group_id>/albums/create', methods=['GET', 'POST'])
def create_album(group_id):
    # form = None
    # if form.validate_on_submit():
    #     group = Group.query.filter_by(id=group_id).first()
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
    # return render_template('create_album.html', title='Create Album', form=form)
    ...


@app.route('/groups/<int:group_id>/albums/<int:album_id>/edit', methods=['GET', 'POST'])
def edit(group_id, album_id):
    form = None
    if form.validate_on_submit():
        group = Group.query.filter_by(id=group_id).first()
        if not group:
            flash('Група не знайдена', 'danger')
            return redirect(url_for('add_song'))

        album = group.albums.filter_by(id=album_id).first()
        if not album:
            flash('Альбом не знайдено', 'danger')
            return redirect(url_for('add_song'))

        album.image = form.image.data
        album.label = form.label.data

        song = Song(
            title=form.title.data,
            album=album,
            media=form.media.data
        )

        db.session.add(song)
        db.session.commit()
        flash(f'Пісня успішно додана до альбому {album.label}!', 'success')
        return redirect(url_for('edit'))
    return render_template('edit.html', title='', form=form)









