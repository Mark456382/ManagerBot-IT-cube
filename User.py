from aiogram.dispatcher.filters.state import State, StatesGroup

class User(StatesGroup):
    worker = State()
    employer = State()
    family = State()
    self = State()
# try:
#     ...
# except BaseException as e:
#     query = f'https://stackoverflow.com/search?q={"+".join(e.split())}'
#     print(query)