from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    value = State()
