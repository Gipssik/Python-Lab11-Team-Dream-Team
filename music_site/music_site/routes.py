from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user

from . import app, bcrypt, db
from .forms import RegistrationForm, LoginForm, GroupForm, AlbumForm, EditAlbumForm, UpdateUserInfoForm, UpdateAlbumInfoForm
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
        if not isinstance(form.image.data, str):
            current_user.image = save_image(form.image.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        db.session.merge(current_user)
        db.session.commit()
        flash('Ваш аккаунт оновлено!', 'success')
        return redirect(url_for('account'))

    return render_template('account.html', title='Account', form=form)


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
    group = Group.query.get_or_404(group_id)
    return render_template('group_page.html', title=group.name, group=group)


@app.route('/groups/<int:group_id>/delete', methods=['GET'])
@login_required
def group_delete(group_id):
    group = Group.query.get_or_404(group_id)
    if current_user in group.users:
        albums = db.session.query(Album).filter(Album.group_id == group.id).all()
        for album in albums:
            db.session.query(Song).filter_by(album_id=album.id).delete()
            db.session.delete(album)

        db.session.delete(group)
        db.session.flush()
        db.session.commit()
        flash('Група успішно видалена', 'success')
        return redirect(url_for('home'))
    flash('Ви не є учасником групи', 'danger')
    return redirect(url_for('group_page', group_id=group_id))


@app.route('/groups/<int:group_id>/albums/create', methods=['GET', 'POST'])
@login_required
def create_album(group_id):
    form = AlbumForm()
    if form.validate_on_submit():
        group = Group.query.get_or_404(group_id)

        if current_user not in group.users:
            flash('Ви не є учасником групи', 'danger')
            return redirect(url_for('group_page', group_id=group_id))

        album = Album(
            label=form.label.data,
            group=group
        )
        if form.img.data:
            album.image = save_image(form.img.data)

        db.session.add(album)
        db.session.commit()
        flash('Альбом успішно створено!', 'success')
        return redirect(url_for('group_page', group_id=group_id))
    return render_template('create_album.html', title='Створення Альбому', form=form)


@app.route('/albums/<int:album_id>', methods=['GET', 'POST'])
@login_required
def album_page(album_id):
    album = Album.query.get_or_404(album_id)
    return render_template('album_page.html', title=album.label, album=album)


@app.route('/albums/<int:album_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    album = Album.query.get_or_404(album_id)
    print(album.__dict__)
    form = UpdateAlbumInfoForm(obj=album)

    if current_user not in album.group.users:
        flash('Ви не є учасником групи', 'danger')
        return redirect(url_for('album_page', album_id=album_id))

    if form.validate_on_submit():
        if form.label.data:
            album.label = form.label.data
        if form.image.data:
            album.image = save_image(form.image.data)

        db.session.commit()

        flash(f'Альбом "{album.label}" оновлено!', 'success')
        return redirect(url_for('album_page', album_id=album_id))
    return render_template('edit_album.html', title='Редагування', form=form)


@app.route('/albums/<int:album_id>/add-song', methods=['GET', 'POST'])
@login_required
def add_song(album_id):
    form = EditAlbumForm()
    album = Album.query.get_or_404(album_id)

    if current_user not in album.group.users:
        flash('Ви не є учасником групи', 'danger')
        return redirect(url_for('album_page', album_id=album_id))

    if form.validate_on_submit():
        if form.title.data and form.media.data:
            song = Song(
                title=form.title.data,
                album=album,
                media=save_audio(form.media.data)
            )
            db.session.add(song)
            db.session.commit()
        
        flash(f'Альбом "{album.label}" оновлено!', 'success')
        return redirect(url_for('album_page', album_id=album_id))
    return render_template('edit_music.html', title='Редагування', form=form)


@app.route('/albums/<int:album_id>/delete', methods=['GET'])
@login_required
def album_delete(album_id):
    album = Album.query.get_or_404(album_id)
    if current_user in album.group.users:
        db.session.query(Song).filter_by(album_id=album.id).delete()
        db.session.delete(album)
        db.session.flush()
        db.session.commit()
        flash('Альбому успішно видалено', 'success')
        return redirect(url_for('group_page', group_id=album.group_id))
    flash('Ви не є учасником групи', 'danger')
    return redirect(url_for('album_page', album_id=album_id))


@app.route('/songs/<int:song_id>/delete', methods=['GET'])
@login_required
def song_delete(song_id):
    song = Song.query.get_or_404(song_id)
    if current_user in song.album.group.users:
        db.session.delete(song)
        db.session.commit()
        flash('Альбому успішно видалено', 'success')
        return redirect(url_for('album_page', album_id=song.album_id))
    flash('Ви не є учасником групи', 'danger')
    return redirect(url_for('album_page', album_id=song.album_id))
