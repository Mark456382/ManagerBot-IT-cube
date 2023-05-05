from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# тут для вас тоже ничего интересного нет
# здесь создается шлюз для подключения к базе данных
engine = create_engine('postgresql+psycopg2://postgres:1234@localhost/ManageBot-IT-cube')
DeclarativeBase = declarative_base()
DeclarativeBase.metadata.create_all(engine)