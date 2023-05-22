from sqlalchemy import Column, Integer, String, ForeignKey
from base.settings import DeclarativeBase

class Users(DeclarativeBase):
    """Класс регистрации таблицы управлющих"""
    
    __tablename__ = 'users'

    user_id = Column('user_id', Integer, primary_key=True)
    user_name =  Column('user_name', String)


    def __str__(self):
        return ''