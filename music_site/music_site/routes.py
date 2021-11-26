from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user

from . import app, bcrypt, db
from .forms import RegistrationForm, LoginForm, GroupForm, AlbumForm, EditAlbumForm, UpdateUserInfoForm
from .models import User, Group, Album, Song, Role
from .services import save_image, save_audio



@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    musicians = Group.query.all()
    return render_template('home.html', title='Головна', musicians=musicians)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        if form.musician.data:
            role = Role.query\
                .filter_by(title="Musician").first()
        else:
            role = Role.query\
                .filter_by(title="User").first()

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()
        flash('Аккаунт успішно створено!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Реєстрація', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Невдача. Перевірте логін і пароль.', 'danger')
    return render_template('login.html', title='Логін', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserInfoForm(obj=current_user)
    if form.validate_on_submit():
        if form.image.data:
            current_user.image = save_image(form.image.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        db.session.commit()
        flash('Ваш аккаунт оновлено!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image = url_for('static', filename=f'img/{current_user.image}')
    return render_template('account.html', title='Account', image=image, form=form)


@app.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()
    if form.validate_on_submit():

        group = Group(
            name=form.name.data,
            content=form.content.data,
        )

        if form.img.data:
            group.image = save_image(form.img.data)

        for username in form.users.data.split(", "):
            user = User.query.filter_by(username=username).first()
            if not user:
                flash('Користувача не знайдено', 'danger')
                return redirect(url_for('create_group'))
            group.users.append(user)

        db.session.add(group)
        db.session.commit()
        flash('Групу успішно створено!', 'success')
        return redirect(url_for('home'))
    return render_template('create_group.html', title='Створення Групи', form=form)


@app.route('/groups/<int:group_id>')
@login_required
def group_page(group_id):
    group = Group.query.get(group_id)
    if not group:
        flash('Група не знайдена', 'danger')
        return redirect(url_for('home'))

    return render_template('group_page.html', title=group.name, group=group)


@app.route('/groups/<int:group_id>/albums/create', methods=['GET', 'POST'])
@login_required
def create_album(group_id):
    form = AlbumForm()
    if form.validate_on_submit():
        group = Group.query.get(group_id)
        if not group:
            flash('Група не знайдена', 'danger')
            return redirect(url_for('create_album', group_id=group_id))

        album = Album(
            label=form.label.data,
            group=group
        )
        if form.img.data:
            album.image = save_image(form.img.data)

        db.session.add(album)
        db.session.commit()
        flash('Альбом успішно створено!', 'success')
        return redirect(url_for('home'))
    return render_template('create_album.html', title='Створення Альбому', form=form)


@app.route('/albums/<int:album_id>', methods=['GET', 'POST'])
@login_required
def album_page(album_id):
    album = Album.query.filter_by(id=album_id).first()
    if not album:
        flash('Альбом не знайдено', 'danger')
        return redirect(url_for('home'))
    return render_template('album_page.html', title=album.label, album=album)


@app.route('/albums/<int:album_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    form = EditAlbumForm()
    album = Album.query.filter_by(id=album_id).first()

    if not album:
        flash('Альбом не знайдено', 'danger')
        return redirect(url_for('home'))

    if form.validate_on_submit():
        if current_user not in album.group.users:
            flash('Ви не автор альбому', 'danger')
            return redirect(url_for('home'))

        if form.img.data:
            album.image = save_image(form.img.data)

        album.label = form.label.data
        if form.title.data and form.media.date:
            song = Song(
                title=form.title.data,
                album=album,
                media=save_audio(form.media.data)
            )
            db.session.add(song)

        db.session.commit()
        flash(f'Альбом "{album.label}" оновлено!', 'success')

        return redirect(url_for('edit_album'))
    return render_template('edit.html', title='Редагування', form=form)
