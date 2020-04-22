from pyperclip import copy
from flask import Flask, render_template, redirect, request, abort
#  from data_db import db_session
from data_db.db_test_session import db_session, init_db
from api import blueprint
from data_db.users import User
from data_db.programs import Program
from data_db.scenarios import Scenario
from data_db.operating_system import Function
from generator_key import generator_password
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms.login import LoginForm
from forms.registration import RegistrationForm
from forms.scenario import ScenarioForm
from forms.functions import FunctionsForm
from forms.program import ProgramForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'v!hT49JOc,Nob_Hp5urgx.D8Adfy1zS6n?YBPCsM'
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(blueprint)


# Загрузка игрока для входа
@login_manager.user_loader
def load_user(user_id):
    session = db_session
    #  session = db_session.create_session()
    return session.query(User).get(user_id)


# Главная страница
@app.route('/')
def main():
    return render_template('main.html')


# Выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Вход на сайт
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #  session = db_session.create_session()
        #  user = session.query(User).filter(User.email == form.email.data).first()
        user = db_session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', form=form)


# Регистрация на сайте
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_repeat.data:
            return render_template('registration.html', form=form, message="Пароли не совпадают")
        #  session = db_session.create_session()
        if db_session.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', form=form, message="Такой пользователь уже есть")

        function_add = Function(
            shut_down=True,
            reboot=True,
            sleep_mode=True
        )

        user = User(
            email=form.email.data,
            key_user=generator_password(50)
        )

        user.set_password(form.password.data)
        user.functions.append(function_add)
        db_session.add(user)
        db_session.commit()
        return redirect('/login')
    return render_template('registration.html', form=form)


# Блок с информацией
@app.route('/information')
@login_required
def information():
    #  session = db_session.create_session()
    user = db_session.query(User).filter(User.email == current_user.email).first()
    key_user = user.key_user
    return render_template('information.html', key_user=key_user)


# Программы, которые есть на ПК
@app.route('/programs')
@login_required
def program():
    form = ProgramForm()
    #  session = db_session.create_session()
    #  session = db_session
    all_programs = db_session.query(Program).filter(Program.user_id == current_user.id).all()
    return render_template('programs.html', form=form, all_programs=all_programs)


# Добавление программ
@app.route('/programs/add', methods=['GET', 'POST'])
@login_required
def add_program():
    form = ProgramForm()
    if form.validate_on_submit():
        #  session = db_session.create_session()
        user = db_session.query(User).filter(User.email == current_user.email).first()
        new_program = Program(
            name_program=form.name_program.data,
            path_program=form.path_program.data
        )
        all_programs = db_session.query(Program).filter(Program.user_id == current_user.id).all()
        if check_name_progam(form.name_program.data, new_program, all_programs):
            return render_template('programs.html', form=form, condition="add",
                                   message="Программа с таким именем уже есть")
        user.programs.append(new_program)
        db_session.commit()
        return redirect('/programs')
    # session = db_session.create_session()
    return render_template('programs.html', form=form, condition="add")


# Редактирование имени и пути программы
@app.route('/programs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_program(id):
    form = ProgramForm()
    if request.method == "GET":
        #  session = db_session.create_session()
        program = db_session.query(Program).filter(Program.id == id, Program.user == current_user).first()

        if program:
            form.name_program.data = program.name_program
            form.path_program.data = program.path_program
        else:
            abort(404)
    if form.validate_on_submit():
        #  session = db_session.create_session()
        program = db_session.query(Program).filter(Program.id == id, Program.user == current_user).first()
        if program:
            all_programs = db_session.query(Program).filter(Program.user_id == current_user.id).all()
            if check_name_progam(form.name_program.data, program, all_programs):
                return render_template('programs.html', form=form, condition="edit",
                                       message="Программа с таким именем уже есть")

            program.name_program = form.name_program.data
            program.path_program = form.path_program.data
            db_session.commit()
            return redirect('/programs')
        else:
            abort(404)
    return render_template('programs.html', form=form, condition="edit")


# Данный метод проверяет, есть ли такая программа или нет
def check_name_progam(name_program_new, program, all_programs):
    for i in all_programs:
        if name_program_new == i.name_program and program.id != i.id:
            return True
    return False


# Удаление программы
@app.route('/programs/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_program(id):
    #  session = db_session.create_session()
    program = db_session.query(Program).filter(Program.id == id, Program.user == current_user).first()
    if program:
        db_session.delete(program)
        db_session.commit()
    else:
        abort(404)
    return redirect('/programs')


# Копирование пути
# @app.route('/programs/copy_path/<int:id>', methods=['GET', 'POST'])
# @login_required
# def copy_path_program(id):
#     #  session = db_session.create_session()
#     program = db_session.query(Program).filter(Program.id == id, Program.user == current_user).first()
#     if program:
#         copy(str(program.path_program))
#     else:
#         abort(404)
#     return redirect('/programs')


# Копирование ключа
# @app.route('/information/copy_key', methods=['GET', 'POST'])
# @login_required
# def copy_key_user():
#     session = db_session.create_session()
#     user = session.query(User).get(current_user.id)
#     if user:
#         copy(str(user.key_user))
#     else:
#         abort(404)
#     return redirect('/information')


# Сценарии, которые создает пользователь
@app.route('/scenarios')
@login_required
def scenarios():
    form = ScenarioForm()
    res_scenarios_list = get_scenarios()
    #  print(res_scenarios_list)
    return render_template('scenarios.html', form=form, all_scenarios=res_scenarios_list)


# Создание сценария
@app.route('/scenarios/add')
@login_required
def add_scenarios():
    form = ScenarioForm()
    return render_template('scenarios.html', form=form, condition="add")


# Редактирование сценария
@app.route('/scenarios/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_scenarios(id):
    form = ScenarioForm()
    res_scenario = get_scenario_id(id)
    programs = res_scenario['programs']

    if request.method == "GET":
        #  session = db_session.create_session()
        scenario = db_session.query(Scenario).filter(Scenario.id == id, Scenario.user == current_user).first()
        #  all_programs = db_session.query(Program).filter(Program.user == current_user).all()
        if scenario:
            form.name_scenario.data = scenario.name_scenario
        else:
            abort(404)

    if form.validate_on_submit():
        #  session = db_session.create_session()
        program = db_session.query(Program).filter(Program.id == id, Program.user == current_user).first()
        if program:
            program.name_program = form.name_program.data
            program.path_program = form.path_program.data
            db_session.commit()
            return redirect('/programs')
        else:
            abort(404)
    #  session = db_session.create_session()
    all_programs = db_session.query(Program).filter(Program.user == current_user).all()
    return render_template('scenarios.html', form=form, condition="edit", programs=programs, all_programs=all_programs, id=id)


# Удаление сценария
@app.route('/scenarios/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_scenarios(id):
    #  session = db_session.create_session()
    scenario = db_session.query(Scenario).filter(Scenario.id == id, Scenario.user == current_user).first()
    if scenario:
        db_session.delete(scenario)
        db_session.commit()
    else:
        abort(404)
    return redirect('/scenarios')


# Возвращает всю информацию о сценариях
def get_scenarios():
    #  session = db_session.create_session()
    all_programs = db_session.query(Program).filter(Program.user_id == current_user.id).all()
    all_scenarios = db_session.query(Scenario).filter(Scenario.user_id == current_user.id).all()
    res_scenarios_list = []
    for scenario in all_scenarios:
        list_programs = scenario.programs.split()
        res_program_list = []
        for program in all_programs:
            for j in list_programs:
                if int(j) == program.id:
                    res_program_list.append(program)
        res_scenarios_list.append({
            'scenario': scenario,
            'programs': res_program_list
        })
    return res_scenarios_list


# Возвращает сценарий по id
def get_scenario_id(id):
    #  session = db_session.create_session()
    scenario = db_session.query(Scenario).filter(Scenario.id == id, Scenario.user == current_user).first()
    res_scenarios_list = get_scenarios()
    for res_scenario in res_scenarios_list:
        if res_scenario['scenario'].id == scenario.id:
            return res_scenario
    return None


# Работа с операционной системой
@app.route('/operating_system', methods=['GET', 'POST'])
def reminding():
    form = FunctionsForm()
    if request.method == 'GET':
        #  session = db_session.create_session()
        functions = db_session.query(Function).filter(Function.user == current_user).first()

        if functions:
            form.shut_down.data = functions.shut_down
            form.reboot.data = functions.reboot
            form.sleep_mode.data = functions.sleep_mode

        else:
            abort(404)
    if form.validate_on_submit():
        #  session = db_session.create_session()
        functions = db_session.query(Function).filter(Function.user == current_user).first()

        if functions:
            functions.shut_down = form.shut_down.data
            functions.reboot = form.reboot.data
            functions.sleep_mode = form.sleep_mode.data
            db_session.commit()
            return redirect('/operating_system')
        else:
            abort(404)
    return render_template('operating_system.html', form=form)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    #  db_session.global_init()
    init_db()
    app.run(port=5001)
