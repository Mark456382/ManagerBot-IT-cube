import random
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

engine = create_engine('postgresql+psycopg2://postgres:1234@localhost/ManageBot-IT-cube')
DeclarativeBase = declarative_base()
DeclarativeBase.metadata.create_all(engine)


class Executors(DeclarativeBase):
    __tablename__ = 'executors' 

    tg_id = Column('tg_id', Integer, primary_key=True)
    name = Column('name', String)
    manager = Column('manager', Integer)


class Managers(DeclarativeBase):
    __tablename__ = 'managers'

    tg_id = Column('tg_id', Integer, primary_key=True)
    executors = Column('executors', Integer)
    name =  Column('name', String)


class Tasks(DeclarativeBase):
    __tablename__ = 'tasks'

    executor = Column('executor', Integer, primary_key=True)
    task = Column('task', String)


class ManageBot:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session(autoflush=False, bind=engine)

    def add_post_to_executors(self, name):
        post = Executors(tg_id=random.randint(1000, 9999), name=name, manager=random.randint(1000, 9999))
        self.session.add(post)
        self.session.commit()
        return self.session.close()

    def add_post_to_manager(self, name):
        post = Managers(tg_id=random.randint(1000, 9999), executors=random.randint(1000, 9999),name=name)
        self.session.add(post)
        self.session.commit()
        return self.session.close()

    def add_new_task(self, task):
        post = Tasks(task=task, executor=random.randint(1000, 9999))
        self.session.add(post)
        self.session.commit()
        return self.session.close()

    # def get_name_to_docktors(self, pk):
    #     return self.session.query(Docktors).get(pk)

    # def get_name_to_patients(self):
    #     return self.session.query(Patient.name).all()
    
    # def get_screen_to_patients(self):
    #     return self.session.query(Patient.path).all()

    # def get_name_to_references(self):
    #     return self.session.query(References).all()

    # def get_path_to_references(self, pk):
    #     return self.session.query(References.path).filter(References.num_ref == pk).all()

    # def get_id_to_patients(self, name):
    #     return self.session.query(Patient.num_references).filter(Patient.name == name).all()


if __name__ == "__main__":
    db = ManageBot()
    # aa = db.get_id_to_patients('Alex')
    # print(db.get_path_to_references(aa[0][0]))
    # print(db.add_post_to_manager('Alex'))
    db.add_new_task('Принеси воды')
