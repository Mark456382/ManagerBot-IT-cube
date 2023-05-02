from aiogram.dispatcher.filters.state import State, StatesGroup

class User(StatesGroup):
    worker = State()
    employer = State()
    family = State()
    self = State()