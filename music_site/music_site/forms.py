from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.fields.simple import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User


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


