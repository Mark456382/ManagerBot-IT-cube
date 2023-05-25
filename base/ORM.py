# -> tabels import
from base.tabels.executors import Executors
from base.tabels.tasks import Tasks
from base.tabels.managers import Managers
from base.tabels.users import Users
# -> settings import
from base.settings import *
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

        try:
            post = Executors(tg_id=executor_id, name=name, manager=manager_id)
            self.session.add(post)
            self.session.commit()
            return self.session.close()
        except BaseException as e:
            print(f'Что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()


    def add_post_to_manager(self, manager_id: int, name: str, executor_id=None) -> None:
        """ Добавляет нового управляющего в базу и его исполнителей. 
            Если исполнителя не указывать, то по дефолту он будет 0
            
            manager_id - Telegram ID управляющего,\n 
            name - имя управляющего,\n
            executor_id - Telegram ID исполнителя"""

        try:
            post = Managers(tg_id=manager_id, executors=executor_id, name=name)
            self.session.add(post)
            self.session.commit()
            return self.session.close()
        except BaseException as e:
            print(f'Что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()


    def add_new_task(self, task_name: str, task: str, executor_id: int, date: int) -> None:
        """ Добавляет новую задачу определенному исполнителю.

            task - задача которую нужно выполнить,\n
            executor_id - Тeletgam ID исполнителя"""
        try:
            post = Tasks(task_name=task_name, task=task, executor=executor_id, state=False, date=date)
            self.session.add(post)
            self.session.commit()
            return self.session.close()
        except BaseException as e:
            print(f'Что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()

    def get_all_executors(self, manager_id: int) -> list[tuple[int]]:
        """ Получение Telegram ID всех исполнителей определенного управляющего
            
            manager_id - Telegram ID управляющего"""

        try:
            return self.session.query(Executors.tg_id).filter(Executors.manager == manager_id).all()
        except BaseException as e:
            print(f'Что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()

    def get_task(self, executor_id):
        try:
            return self.session.query(Tasks.task_name, Tasks.task, Tasks.date).filter(Tasks.executor == executor_id, Tasks.state == False).all()
        except BaseException as e:
            print(f'Что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()

    def get_manager_for_executor(self, executor_id: int) -> list[tuple]:
        """ Получаем информацию об управляющем 
            определленного исполнителя
            
            executor_id - Telegram ID иссполнителя"""
        
        try:
            return self.session.query(Executors.name, Executors.manager).filter(Executors.tg_id == executor_id).all()
        except BaseException as e:
            return f'Извините, что то пошло не так\nОшибка: {e}'
        finally:
            self.session.close()


    def get_state_for_task(self, executor_id: int) -> list[tuple[bool]]:
        """ Получение текущего состояния задачи
        
            executor_id - Telegram ID исполнителя"""
        
        try:
            return self.session.query(Tasks.state).filter(Tasks.executor == executor_id).all()
        except BaseException as e:
            return f'Извините, что то пошло не так\nОшибка: {e}'
        finally:
            self.session.close()


    def get_date_for_task(self, executor_id: int) -> list[tuple[int]]:
        """ Получаем врмя отведенное на определенную задачу (Возвращает время в часах).
            По дефолту указано 24 часа
            
            executor_id - Telegram ID исполнителя"""
        
        try:
            return self.session.query(Tasks.date).filter(Tasks.executor == executor_id).all()
        except BaseException as e:
            return f'Извините, что то пошло не так\nОшибка: {e}'
        finally:
            self.session.close()

    def get_executor_for_manager(self, manager_id: int):
        try:
            return self.session.query(Managers.executors).filter(Managers.tg_id == manager_id).all()[0][0]
        except BaseException as e:
            return f'Извините, что то пошло не так\nОшибка: {e}'
        finally:
            self.session.close()


    def add_user(self, user_name: str, user_id: int) -> None:
        """ Добавлентие в базу всех пользователей 
            нового человека
            
            user_id = Telegram ID
            user_name = Имя человека"""

        try:
            post = Users(user_name=user_name, user_id=user_id)
            self.session.add(post)
            self.session.commit()
            return self.session.close()
        except BaseException as e:
            print(f'Что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()

    def complete_tasks(self, user_id: int) -> None:
        obj =  self.session.query(Tasks).filter(Tasks.executor == user_id,  Tasks.status == False).first()
        obj.state = True
        self.session.commit()

    def check_user(self, user_name: str) -> list[tuple[int]]:
        try:
            return self.session.query(Users.user_id).filter(Users.user_name == user_name).all()
        except BaseException as e:
            print(f'Извините, что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()

    def get_state_user(self, user_id: str) -> list[tuple[bool]]:
        try:
            return self.session.query(Users.state).filter(Users.user_id == user_id).all()[0][0]
        except BaseException as e:
            print(f'Извините, что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()

    def add_user_state(self, user_id: str, state: bool) -> None:
        obj =  self.session.query(Users).filter(Users.user_id == user_id).first()
        obj.state = state
        self.session.commit()


    def get_username(self, user_id: int) -> list[tuple[int]]:
        try:
            return self.session.query(Users.user_name).filter(Users.user_id == user_id).all()[0][0]
        except BaseException as e:
            print(f'Извините, что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()

    def get_user_id(self, user_name: str) -> None:
        try:
            return self.session.query(Users.user_id).filter(Users.user_name == user_name).all()[0][0]
        except BaseException as e:
            print(f'Извините, что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()

    def reset_executor(self, user_id: int, executor_id: int) -> None:
        obj =  self.session.query(Managers).filter(Managers.tg_id == user_id).first()
        obj.executors = executor_id
        self.session.commit()
