from music_site import app, db
from music_site.models import User, Role

if __name__ == '__main__':
    db.create_all()
    if not User.query.all():
        r = Role(title='Admin')
        a = User(username='admin', email='admin@admin.com', password='admin', role=r)
        db.session.add(r)
        db.session.add(a)
        db.session.commit()

    app.run(debug=True)
