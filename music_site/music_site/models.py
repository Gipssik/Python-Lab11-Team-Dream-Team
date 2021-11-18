from flask_login import UserMixin

from . import db, login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=False, nullable=False)
    image = db.Column(db.String(64), unique=False, nullable=False, default='default.jpg')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)

    def __repr__(self):
        return f'User("{self.username}", "{self.email}")'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f'Role("{self.title}")'


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=False, nullable=False)
    media = db.Column(db.String(64), unique=False, nullable=False)
    image = db.Column(db.String(64), unique=False, nullable=False, default='default.jpg')
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)

    def __repr__(self):
        return f'Song("{self.title}")'


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=False, nullable=False)
    data_created = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(64), unique=False, nullable=False, default='default.jpg')
    songs = db.relationship('Song', backref='album', lazy=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    def __repr__(self):
        return f'Album("{self.label}")'


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=False, nullable=False)
    content = db.Column(db.String(1000), unique=False, nullable=False)
    data_created = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(64), unique=False, nullable=False, default='default.jpg')
    users = db.relationship('User', backref='group', lazy=True)
    albums = db.relationship('Album', backref='group', lazy=True)

    def __repr__(self):
        return f'Group("{self.name}")'
