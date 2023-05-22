from aiogram.dispatcher.filters.state import State, StatesGroup


class Executor(StatesGroup):
    name = State()
    manager = State()


class Manager(StatesGroup):
    name = State()
    executor = State()

class Formyself(StatesGroup):
    name = State()
    description = State()
    time = State()
# try:
#     ...
# except BaseException as e:
#     query = f'https://stackoverflow.com/search?q={"+".join(e.split())}'
#     print(query)