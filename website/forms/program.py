from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class ProgramForm(FlaskForm):
    name_program = StringField("Name Program", validators=[DataRequired()])
    path_program = StringField("Path Program", validators=[DataRequired()])
    add_btn = SubmitField("Добавить")
    change_btn = SubmitField("Изменить")
