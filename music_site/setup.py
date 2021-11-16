from music_site import app, db
from music_site.models import User

if __name__ == '__main__':
    db.create_all()
    if not User.query.all():
        a = User(username='admin', email='admin@admin.com', password='admin')
        db.session.add(a)
        db.session.commit()

    app.run(debug=True)
