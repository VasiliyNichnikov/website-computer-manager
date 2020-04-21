import flask
from flask import jsonify, request
from data_db import db_session
from data_db.users import User
from flask_login import current_user
from data_db.programs import Program
from data_db.scenarios import Scenario
from data_db.operating_system import Function


blueprint = flask.Blueprint('api', __name__, template_folder="template")


# Данный метод добавляет ключ приложения в БД
@blueprint.route('/add_key_program', methods=['POST'])
def add_key_program():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['key_user']:
        return jsonify({'error': 'not_key_user'})
    key_user = request.json['key_user']
    session = db_session.create_session()
    user = session.query(User).filter(User.key_user == key_user).first()
    if not user:
        return jsonify({'error': 'user_not_found'})
    if user.program_active:
        return jsonify({'error': 'key_active'})
    user.program_active = True
    session.commit()
    return jsonify({'success': 'add_program'})


# Данный метод отключает приложение от БД сервера
@blueprint.route('/exit_key_program', methods=['POST', 'GET'])
def exit_key_program():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['key_user']:
        return jsonify({'error': 'not_key_user'})
    key_user = request.json['key_user']
    session = db_session.create_session()
    user = session.query(User).filter(User.key_user == key_user).first()
    if not user:
        return jsonify({'error': 'user_not_found'})
    if not user.program_active:
        return jsonify({'error': 'key_not_active'})
    user.program_active = False
    session.commit()
    return jsonify({'success': 'exit_program_success'})


# Данный метод добавляет ключ бота в БД
@blueprint.route('/add_key_bot', methods=['POST'])
def add_key_bot():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['key_user'] or not request.json['id_user_vk']:
        return jsonify({'error': 'Not key_user'})
    key_user = request.json['key_user']
    id_user_vk = request.json['id_user_vk']
    session = db_session.create_session()
    user = session.query(User).filter(User.key_user == key_user).first()
    if not user:
        return jsonify({'error': 'error_not_found_key'})
    if user.bot_active:
        return jsonify({'error': 'error_key_activated'})
    user.bot_active = True
    user.id_user_vk = id_user_vk
    session.commit()
    return jsonify({'success': 'OK'})


# Данный метод отключает бота от БД сервера
@blueprint.route('/exit_key_bot', methods=['POST', 'GET'])
def exit_key_bot():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['key_user']:
        return jsonify({'error': 'Not key_user'})
    key_user = request.json['key_user']
    session = db_session.create_session()
    user = session.query(User).filter(User.key_user == key_user).first()
    if not user:
        return jsonify({'error': 'error_not_found_key'})
    if not user.bot_active:
        return jsonify({'error': 'error_key_not_activated'})
    user.bot_active = False
    user.id_user_vk = None
    session.commit()
    return jsonify({'success': 'exit_bot_success'})


# Данный метод изменяет путь программы, чтобы клиент мог открыть ее
@blueprint.route('/change_path_program', methods=['POST'])
def change_path_program():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['key_user'] or not request.json['name_program']:
        return jsonify({'error': 'Not key_user or name_program'})
    session = db_session.create_session()
    key_user = request.json['key_user']
    name_program = request.json['name_program']
    #  return jsonify({"f": name_program})
    # Program.name_program == name_program
    user = session.query(User).filter(User.key_user == key_user).first()
    program = session.query(Program).filter(Program.user_id == user.id, Program.name_program == name_program).first()
    #  program = session.query(Program).filter(Program.name_program == name_program).first()
    if not user:
        return jsonify({'error': 'user_not_found'})
    if not program:
        return jsonify({'error': 'program_not_found'})
    if not user.bot_active:
        return jsonify({'error': 'bot not active'})
    user.path_program_select = program.path_program
    session.commit()
    return jsonify({'success': 'path_program_change_success'})


# Данный метод меняет название сценария, который нужно запустить
@blueprint.route('/change_name_scenario', methods=['POST', 'GET'])
def change_name_scenario():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['key_user'] or not request.json['name_scenario']:
        return jsonify({'error': 'Not key_user or name_scenario'})
    session = db_session.create_session()
    key_user = request.json['key_user']
    name_scenario = request.json['name_scenario']
    user = session.query(User).filter(User.key_user == key_user).first()
    if not user:
        return jsonify({'error': 'user_not_found'})
    scenario = session.query(Scenario).filter(Scenario.user_id == user.id, Scenario.name_scenario == name_scenario).first()
    if not scenario:
        return jsonify({'error': 'scenario_not_found'})
    user.scenario_select = scenario.name_scenario
    session.commit()
    return jsonify({'success': 'name_scenario_change_success'})

# Данный метод меняет функцию (Выключить, перезагрузить или включить спящий режим на ПК)
@blueprint.route('/change_pc_function', methods=['POST', 'GET'])
def change_pc_function():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['key_user'] or not request.json['function']:
        return jsonify({'error': 'Not key_user or function'})
    session = db_session.create_session()
    key_user = request.json['key_user']
    name_function = request.json['function']
    user = session.query(User).filter(User.key_user == key_user).first()
    if not user:
        return jsonify({'error': 'user_not_found'})
    result_check_pc_function = check_pc_function(user, name_function)
    if result_check_pc_function == 'success':
        user.select_pc_function = name_function
        session.commit()
        return jsonify({'success': 'name_function_change_success'})
    else:
        return jsonify({'error': result_check_pc_function})


# Данный метод проверяет, есть ли такая функция на сервере и включена она пользователем
def check_pc_function(user, fucnction):
    session = db_session.create_session()
    user_functions = session.query(Function).filter(Function.user == user).first()
    functions = {
        'shutdown': user_functions.shut_down,
        'reboot': user_functions.reboot,
        'sleep_mode': user_functions.sleep_mode
    }
    if fucnction not in functions.keys():
        return 'function_not_found'
    select_function = functions[fucnction]
    if select_function is False:
        return 'function_lock'
    return 'success'


# Данный метод получает все функции, которые отправил бот
@blueprint.route('/get_all_functions_client', methods=['POST', 'GET'])
def get_all_functions_client():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['key_user']:
        return jsonify({'error': 'not_found_key_user'})
    session = db_session.create_session()
    key_user = request.json['key_user']
    user = session.query(User).filter(User.key_user == key_user).first()
    if not user:
        return jsonify({'error': 'user_not_found'})
    # Получение информации
    path_program_select = user.path_program_select
    scenario_select = user.scenario_select
    select_pc_function = user.select_pc_function
    scenario = session.query(Scenario).filter(Scenario.name_scenario == scenario_select, Scenario.user == user).first()
    all_programs = session.query(Program).filter(Program.user == user).all()
    # Очистка информации, чтобы не было повторного запуска
    user.path_program_select = None
    user.scenario_select = None
    user.select_pc_function = None
    session.commit()
    return jsonify({'path_program_select': path_program_select, 'scenario_select': get_list_programs(scenario, all_programs), 'select_pc_function': select_pc_function})



# Данный метод возвращает список путей к программам
def get_list_programs(scenario, all_programs):
    if not scenario or not all_programs:
        return None
    list_programs = []
    programs_scenario = scenario.programs.split()
    for program_scenario in programs_scenario:
        for program in all_programs:
            if program.id == int(program_scenario):
                list_programs.append(str(program.path_program))
    return list_programs


# Данный метод получает информацию о программе, которую надо запустить на ПК
@blueprint.route('/get_start_program', methods=['POST'])
def get_start_program():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['key_user']:
        return jsonify({'error': 'Not key_user'})
    session = db_session.create_session()
    key_user = request.json['key_user']
    user = session.query(User).filter(User.key_user == key_user).first()
    path_program_select = user.path_program_select
    user.path_program_select = ""
    session.commit()
    return jsonify({'path_program': [path_program_select]})


# Проверка пользователя, есть ли у него ключ или нет
@blueprint.route('/check_key_user', methods=['POST'])
def check_key_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['id_user_vk']:
        return jsonify({'error': 'Not id_user_vk'})
    id_user_vk = request.json['id_user_vk']
    session = db_session.create_session()
    user = session.query(User).filter(User.id_user_vk == id_user_vk).first()
    if not user:
        return jsonify({'error': 'not_user'})
    key_user = user.key_user
    return jsonify({'key_user': key_user})


# Данный метод возвращает программы, которые есть у пользователя на сайте
@blueprint.route('/get_programs_for_scenarios', methods=['GET'])
def get_programs_for_scenarios():
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    if not user:
        return jsonify({'error': 'user not found'})
    programs = user.programs
    if not programs:
        return jsonify({'error': 'programs not found'})
    list_names_programs = []
    for i in programs:
        list_names_programs.append(i.name_program)
    return jsonify({'programs': list_names_programs})


# Данный метод получает программы, которые нужно добавить в сценарий
@blueprint.route('/create_new_scenario', methods=['GET', 'POST'])
def create_new_scenario():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['programs'] or not request.json['name_scenario']:
        return jsonify({'error': 'Убедитесь, вы добавили программы и ввели название сценария'})
    programs_add_scenario = request.json['programs']
    name_scenario = request.json['name_scenario']
    session = db_session.create_session()
    programs = get_programs(programs_add_scenario)

    scenario = Scenario(
        name_scenario=name_scenario,
        programs=programs
    )
    all_scenarios = session.query(Scenario).filter(Scenario.user == current_user).all()

    if check_scenario(name_scenario, all_scenarios) == "error":
        return jsonify({'error': 'Сценарий с таким именем уже существует'})
    if check_programs(programs_add_scenario) == "error_duplication":
        return jsonify({'error': 'Убедитесь, что программы не повторяются'})
    if check_programs(programs_add_scenario) == "error_len":
        return jsonify({'error': 'Убедитесь, что вы заполнили все поля с программами'})

    user = session.query(User).get(current_user.id)
    user.scenarios.append(scenario)
    session.commit()
    return jsonify({'success': 'OK'})


# Данный метод получает программы и редактирует сценарий
@blueprint.route('/edit_scenario', methods=['GET', 'POST'])
def edit_scenario():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['programs'] or not request.json['name_scenario'] or not request.json['id']:
        return jsonify({'error': 'Убедитесь, вы добавили программы и ввели название сценария'})
    session = db_session.create_session()
    id = int(request.json['id'])
    name_scenario = request.json['name_scenario']
    programs_add_scenario = request.json['programs']
    programs = get_programs(programs_add_scenario)
    scenario = session.query(Scenario).filter(Scenario.id == id, Scenario.user == current_user).first()
    if not scenario:
        return jsonify({'error': 'Not found scenario'})

    all_scenarios = session.query(Scenario).filter(Scenario.user == current_user).all()

    if check_scenario(name_scenario, all_scenarios) == "error":
        return jsonify({'error': 'Сценарий с таким именем уже существует'})
    if check_programs(programs_add_scenario) == "error_duplication":
        return jsonify({'error': 'Убедитесь, что программы не повторяются'})
    if check_programs(programs_add_scenario) == "error_len":
        return jsonify({'error': 'Убедитесь, что вы заполнили все поля с программами'})

    scenario.name_scenario = name_scenario
    scenario.programs = programs
    session.commit()
    return jsonify({'success': 'OK'})


# Возвращает программы, которые есть у пользователя
@blueprint.route('/get_all_programs_user', methods=['GET', 'POST'])
def get_all_programs_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['id_user_vk']:
        return jsonify({'error': 'user_not_found'})
    session = db_session.create_session()
    id_user_vk = request.json['id_user_vk']
    user = session.query(User).filter(User.id_user_vk == id_user_vk).first()
    if not user:
        return jsonify({'error': 'user_not_found'})
    programs = session.query(Program).filter(Program.user == user).all()
    if not programs:
        return jsonify({'error': 'programs_not_found'})
    programs_list = get_names_programs(programs)
    return jsonify({'success': programs_list})


# Возвращает сценарии, которые есть у пользователя
@blueprint.route('/get_all_scenarios_user', methods=['GET', 'POST'])
def get_all_scenarios_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not request.json['id_user_vk']:
        return jsonify({'error': 'user_not_found'})
    session = db_session.create_session()
    id_user_vk = request.json['id_user_vk']
    user = session.query(User).filter(User.id_user_vk == id_user_vk).first()
    if not user:
        return jsonify({'error': 'user_not_found'})
    scenarios = session.query(Scenario).filter(Scenario.user == user).all()
    if not scenarios:
        return jsonify({'error': 'scenarios_not_found'})
    scenarios_list = get_names_programs(scenarios)
    return jsonify({'success': scenarios_list})


# Возвращает имена всех сценарий, которые есть у пользователя
def get_names_scenarios(scenarios):
    names_list = []
    for i in scenarios:
        names_list.append(i.name_program)
    return names_list


# Возвращает имена программ, которые есть у пользователя 
def get_names_programs(programs):
    names_list = []
    for i in programs:
        names_list.append(i.name_program)
    return names_list

# Возвращает сами программы
def get_programs(programs_add_scenario, return_list=False):
    list_programs = []
    session = db_session.create_session()
    programs_user = session.query(Program).filter(Program.user_id == current_user.id).all()
    for program in programs_user:
        for program_add in programs_add_scenario:
            if program.name_program == program_add:
                list_programs.append(str(program.id))
    if not return_list:
        return " ".join(list_programs)
    return list_programs


# Проверяет, можно ли добавлять сценарий (Проверка имени сценария)
def check_scenario(name_scenario, all_scenarios):
    for i in all_scenarios:
        if name_scenario == i.name_scenario:
            return "error"
    return "success"


# Проверяет, можно ли добавить сценарий (Проверка на дублирование программ)
def check_programs(programs_add_scenario):
    list_programs = [int(i) for i in get_programs(programs_add_scenario, True)]
    new_list = []
    if len(list_programs) == 0:
        return "error_len"
    for i in list_programs:
        if i in new_list:
            return "error_duplication"
        new_list.append(i)
    return "success"


