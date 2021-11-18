from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, FieldList
# from wtforms.fields.simple import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User, Group


class RegistrationForm(FlaskForm):
    username = StringField("Ім\'я: ", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Почта: ", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=100)])
    confirm_password = PasswordField(
        'Повторіть пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Таке ім\'я вже існує')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Така пошта вже існує')


class LoginForm(FlaskForm):
    username = StringField("Ім\'я: ", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    remember = BooleanField("Запам\'ятати: ")
    submit = SubmitField("Війти")


class GroupForm(FlaskForm):
    name = StringField("Ім\'я групи: ", validators=[DataRequired(), Length(min=1, max=20)])
    users = StringField("Ім\'я співака(ів): ", validators=[DataRequired(), Length(min=1, max=20)])
    img = FileField("Фото групи: ", validators=[DataRequired()])
    submit = SubmitField("Добавити")

    def validate_group(self, name):
        name_group = Group.query.filter_by(username=name.data).first()
        if name_group:
            raise ValidationError('Таке ім\'я вже існує')


class AlbumForm(FlaskForm):
    label = StringField("Ім\'я альбому: ", validators=[DataRequired(), Length(min=1, max=30)])
    img = FileField("Обкладинка: ", validators=[DataRequired()])

    def validate_album(self, label):
        label_album = Group.query.filter_by(username=label.data).first()
        if label_album:
            raise ValidationError('Таке ім\'я вже існує')



