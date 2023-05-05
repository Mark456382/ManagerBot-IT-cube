import random
# -> tabels import
from tabels.executors import Executors
from tabels.tasks import Tasks
from tabels.managers import Managers
# -> settings import
from settings import *
# -> sqlalchemy import 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL


class ManageBot:
    """ORM класс для управления базой данных ManageBot-IT-cube"""

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session(autoflush=False, bind=engine)

    def add_post_to_executors(self, executor_id: int, name: str, manager_id: int) -> None:
        """ Добавление в базу нового исполнителя.
            
            executor_id - Telegram ID исполнителя,\n
            name - имя исполнителя,\n
            manager_id - Telegram ID управляющего
            """

        post = Executors(tg_id=executor_id, name=name, manager=manager_id)
        self.session.add(post)
        self.session.commit()
        return self.session.close()

    def add_post_to_manager(self, manager_id: int, name: str, executor_id=None) -> None:
        """ Добавляет нового управляющего в базу и его исполнителей. 
            Если исполнителя не указывать, то по дефолту он будет 0
            
            manager_id - Telegram ID управляющего,\n 
            name - имя управляющего,\n
            executor_id - Telegram ID исполнителя"""

        post = Managers(tg_id=manager_id, executors=executor_id,name=name)
        self.session.add(post)
        self.session.commit()
        return self.session.close()

    def add_new_task(self, task: str, executor_id: int) -> None:
        """ Добавляет новую задачу определенному исполнителю.

            task - задача которую нужно выполнить,\n
            executor_id - Тeletgam ID исполнителя"""
        
        post = Tasks(task=task, executor=executor_id)
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
    db.add_new_task(task='Принеси воды', executor_id=random.randint(1000, 9999))
