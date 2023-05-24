from sqlalchemy import Column, Integer, String, ForeignKey
from base.settings import DeclarativeBase

class Managers(DeclarativeBase):
    """Класс регистрации таблицы управлющих"""
    
    __tablename__ = 'managers'

    tg_id = Column('tg_id', Integer, primary_key=True)
    executors = Column('executors', Integer)
    name =  Column('name', String)

