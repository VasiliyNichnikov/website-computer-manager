import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Program(SqlAlchemyBase):
    __tablename__ = 'programs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_program = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    path_program = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # scenario_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("scenarios.id"))
    # scenario = orm.relation('Scenario')

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
