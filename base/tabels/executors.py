from settings import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey


class Executors(DeclarativeBase):
    """Класс регистрации таблицы с исполнителями"""
    
    __tablename__ = 'executors' 

    tg_id = Column('tg_id', Integer, primary_key=True)
    name = Column('name', String)
    manager = Column('manager', Integer)