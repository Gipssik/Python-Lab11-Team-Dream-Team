from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=False, nullable=False)
    image = db.Column(db.String(64), nullable=False, default='default.jpg')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def __repr__(self):
        return f'User("{self.username}", "{self.email}")'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f'Role("{self.title}")'
