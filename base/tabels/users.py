from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from base.settings import DeclarativeBase

class Users(DeclarativeBase):
    """Класс регистрации таблицы всех пользователей"""
    
    __tablename__ = 'users'

    user_id = Column('user_id', Integer, primary_key=True)
    user_name =  Column('user_name', String)
    state = Column('state', Boolean)
