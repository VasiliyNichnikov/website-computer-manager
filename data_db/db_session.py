import psycopg2
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    #  if not db_file or not db_file.strip():
    #      raise Exception("Необходимо указать файл базы данных.")
    
    conn_str = "postgres://fincvilioztuwy:5529db1105625b5b8c56049348c7393e0e528d202c8a10bd0c0e22f1596a12d6@ec2-54-75-246-118.eu-west-1.compute.amazonaws.com:5432/d85u8gcgigior0"
    #  conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
