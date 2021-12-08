from music_site import app, db, bcrypt
from music_site.models import User, Role

if __name__ == "__main__":
    db.create_all()
    if not User.query.all():
        r_a = Role(title='Admin')
        r_m = Role(title='Musician')
        r_u = Role(title='User')
        a = User(
            username='admin',
            email='admin@admin.com',
            password=bcrypt
                .generate_password_hash('admin'),
            role=r_a
        )
        db.session.add_all([r_a, r_m, r_u, a])
        db.session.commit()
    app.run(debug=True)
