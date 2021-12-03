from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList
# from wtforms.fields.simple import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User, Group, Album, Song
from wtforms.widgets import TextArea


class RegistrationForm(FlaskForm):
    username = StringField("Ім\'я", validators=[
                           DataRequired(), Length(min=3, max=20)])
    email = StringField("Почта", validators=[DataRequired(), Email()])
    musician = BooleanField("Я музикант")
    password = PasswordField("Пароль", validators=[
                             DataRequired(), Length(min=4, max=100)])
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
    username = StringField("Ім\'я ", validators=[
                           DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Пароль ", validators=[DataRequired()])
    submit = SubmitField("Увійти")


class GroupForm(FlaskForm):
    name = StringField("Ім\'я групи: ", validators=[
                       DataRequired(), Length(min=1, max=20)])
    users = StringField("Ім\'я співака(ів): ", validators=[DataRequired()])
    img = FileField("Фото групи: ", validators=[FileAllowed(['jpg', 'png'])])
    content = StringField("Опис групи: ", widget=TextArea(),
                          validators=[DataRequired()])
    submit = SubmitField("Добавити")

    def validate_group(self, name):
        name_group = Group.query.filter_by(name=name.data).first()
        if name_group:
            raise ValidationError('Таке ім\'я вже існує')


class AlbumForm(FlaskForm):
    label = StringField("Ім\'я альбому", validators=[
                        DataRequired(), Length(min=1, max=30)])
    img = FileField("Обкладинка", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Добавити")

    def validate_album(self, label):
        label_album = Album.query.filter_by(lable=label.data).first()
        if label_album:
            raise ValidationError('Таке ім\'я вже існує')


class EditAlbumForm(FlaskForm):
    title = StringField("Назва пісні ", validators=[
                        DataRequired(), Length(min=1, max=30)])
    media = FileField("Пісня ", validators=[
                      FileAllowed(['mp3']), FileRequired()])
    submit = SubmitField("Добавити")


class UpdateAlbumInfoForm(FlaskForm):
    name = StringField("Назва альбому ", validators=[Length(min=1, max=30)])
    image = FileField("Фото альбому ", validators=[
        FileAllowed(['jpg', 'png'])])


class UpdateUserInfoForm(FlaskForm):
    username = StringField("Ім\'я: ", validators=[
                           DataRequired(), Length(min=3, max=20)])
    email = StringField("Почта: ", validators=[DataRequired(), Email()])
    image = FileField("Картинка: ", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Змінити")
