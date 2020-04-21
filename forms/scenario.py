from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class ScenarioForm(FlaskForm):
    name_scenario = StringField("Name Scenario", validators=[DataRequired()])
    # path_program = StringField("Path Program", validators=[DataRequired()])
    add_program_btn = SubmitField("Добавить программу")
    add_scenario_btn = SubmitField("Добавить сценарий")
    change_btn = SubmitField("Изменить")
    # email = StringField("Email", validators=[Email()])
    # password = PasswordField("Пароль", validators=[DataRequired()])
    # remember_me = BooleanField('Запомнить меня')
    # submit = SubmitField("Войти")
    # registration = SubmitField("Зарегестрироваться")