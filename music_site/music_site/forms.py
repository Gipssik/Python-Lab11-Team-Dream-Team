from flask_wtf import FlaskForm

# IMPORT REQUIRED FIELDS
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired, Length


class RegisteringUser(FlaskForm):
    name = StringField("Ім'я: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Запам'ятати: ", default=False)
    submit = SubmitField("Війти")


