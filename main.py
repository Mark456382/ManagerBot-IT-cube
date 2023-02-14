from buttons import *
from config import TOKEN
import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class User(StatesGroup):
    value = State()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(f"Приветствую тебя, {message.from_user.first_name}. " +
                         "Я Бот Менеджер, и я помогу тебе с твоими делами. " +
                         "В какой сфере ты собираешься использовать бота?", reply_markup=keyboard)


@dp.message_handler(Text('Бизнес'))
async def busness(message: types.Message):
    await message.reply('Кем ты являешься?', reply_markup=keyboard_1)


@dp.message_handler(Text('Сотрудник (исполнитель)'))
async def helper(message: types.Message):
    deadline = 1
    task = 1
    if task:
        await message.answer('Ожидайте пока руководитель вас пригласит')
    else:
        await message.answer(f'Ваши задачи до {deadline}: {task}')


@dp.message_handler(Text("Менеджер (управляющий)"))
async def lider_name_input(message: types.Message):
    await User.value.set()
    await message.reply('Введите свое ФИО')


@dp.message_handler(state=User.value)
async def lider_name_save(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text
    await state.finish()

    await message.answer(md.bold(data['value']))


@dp.message_handler(Text('Семья'))
async def family(message: types.Message):
    ...


@dp.message_handler(Text('Для себя'))
async def for_self(message: types.Message):
    ...


@dp.message_handler(content_types=['any'])
async def nonetype_message(message: types.Message):
    await message.reply('Я не понимаю что ты от меня хочешь 😅')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
