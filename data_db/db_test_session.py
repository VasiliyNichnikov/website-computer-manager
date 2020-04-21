from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

conn = "postgres://fincvilioztuwy:5529db1105625b5b8c56049348c7393e0e528d202c8a10bd0c0e22f1596a12d6@ec2-54-75-246-118.eu-west-1.compute.amazonaws.com:5432/d85u8gcgigior0"
engine = create_engine(conn, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
#  Base.query = db_session.query_property()


def init_db():
    from . import __all_models
    Base.metadata.create_all(bind=engine)