from base.settings import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class Tasks(DeclarativeBase):
    """Класс регистарции таблицы с задачами"""
    
    __tablename__ = 'tasks'

    executor = Column('executor', Integer, primary_key=True)
    task = Column('task', String)
    task_name = Column('task_name', String)
    state = Column('state', Boolean)
    date = Column('date', Integer)