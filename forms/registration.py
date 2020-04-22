from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_repeat = PasswordField("Повторите пароль", validators=[DataRequired()])
    read_privacy_policy = BooleanField('Я прочитал (-а) и принимааю', validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")
