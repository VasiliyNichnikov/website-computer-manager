import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    programs = orm.relation("Program", back_populates='user')
    scenarios = orm.relation("Scenario", back_populates='user')
    functions = orm.relation("Function", back_populates='user')
    # id пользователя в вк
    id_user_vk = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Путь к программе, которая выбранна у пользователя
    path_program_select = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Название сценария, который выбрал пользователь
    scenario_select = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Выбранная функция у пользователя (Перезапустить, Выключить или спящий режим у ПК)
    select_pc_function = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Ключ пользователя, который создается при регистрации
    key_user = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Говорит, что бот активирован и пользователь может им пользоваться
    bot_active = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    # Говорит, что программа активированна и пользователь может ей пользоваться
    program_active = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)