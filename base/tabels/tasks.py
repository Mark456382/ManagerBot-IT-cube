from settings import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey


class Tasks(DeclarativeBase):
    """Класс регистарции таблицы с задачами"""
    
    __tablename__ = 'tasks'

    executor = Column('executor', Integer, primary_key=True)
    task = Column('task', String)