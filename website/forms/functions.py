from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class FunctionsForm(FlaskForm):
    shut_down = BooleanField('Завершение работы')
    reboot = BooleanField('Перезагрузка')
    sleep_mode = BooleanField('Спящий режим')
    button_save = SubmitField("Сохранить")