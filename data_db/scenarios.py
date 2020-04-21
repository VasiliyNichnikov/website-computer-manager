import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Scenario(SqlAlchemyBase):
    __tablename__ = 'scenarios'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_scenario = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    programs = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
