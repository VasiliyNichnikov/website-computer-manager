import sqlalchemy
from sqlalchemy import orm
from .db_test_session import Base
#  from .db_session import SqlAlchemyBase


class Function(Base):
    __tablename__ = 'functions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # name_function = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # condition_function = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    shut_down = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    reboot = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    sleep_mode = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
