from music_site import app, db
from music_site.models import User, Role

if __name__ == '__main__':
    db.create_all()
    if not User.query.all():
        r_a = Role(title='Admin')
        r_m = Role(title='Musician')
        r_u = Role(title='User')
        a = User(username='admin', email='admin@admin.com', password='admin', role=r_a)
        db.session.add(r_a)
        db.session.add(r_m)
        db.session.add(r_u)
        db.session.add(a)
        db.session.commit()

    app.run(debug=True)
