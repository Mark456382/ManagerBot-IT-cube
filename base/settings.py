from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# тут для вас тоже ничего интересного нет
# здесь создается шлюз для подключения к базе данных
ENGINE = 'postgresql+psycopg2://postgres:1234@localhost/ManageBot-IT-cube'
engine = create_engine(ENGINE)
DeclarativeBase = declarative_base()
DeclarativeBase.metadata.create_all(engine)