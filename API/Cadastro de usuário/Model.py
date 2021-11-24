from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

USER = 'root'
PASSWORD = ''
HOST = 'localhost'
PORT = '3306'
DB = 'API_teste'


def connection():
    """
    :return: session to communicate with the database
    """
    CONN = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    engine = create_engine(CONN, echo=False)
    Session = sessionmaker(bind=engine)
    return Session


Base = declarative_base()


class User(Base):

    __tablename__ = 'User'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))
    password = Column(String(64))


class Token(Base):

    __tablename__ = 'Token'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    token = Column(String(100))
    time = Column(DateTime, default=datetime.utcnow())


Base.metadata.create_all(create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}', echo=False))
