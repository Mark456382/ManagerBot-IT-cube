from aiogram.dispatcher.filters.state import State, StatesGroup


class Executor(StatesGroup):
    name = State()
    manager = State()


class Manager(StatesGroup):
    name = State()
    executor = State()

class Task(StatesGroup):
    name = State()
    description = State()
    time = State()

class Formyself(StatesGroup):
    name = State()
    description = State()
    time = State()

class Passive(StatesGroup):
    username = State()
    name = State()

class Reset(StatesGroup):
    username = State()
    name = State()
# try:
#     ...
# except BaseException as e:
#     query = f'https://stackoverflow.com/search?q={"+".join(e.split())}'
#     print(query)