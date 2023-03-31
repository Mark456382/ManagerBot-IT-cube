import time

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
    value_2 = State()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(f"Приветствую тебя, {message.from_user.first_name}. " +
                         "Я Бот Менеджер, и я помогу тебе с твоими делами. " +
                         "В какой сфере ты собираешься использовать бота?", reply_markup=keyboard)


@dp.message_handler(Text('Бизнес'))
async def busness(message: types.Message):
    await message.reply('Кем ты являешься?', reply_markup=keyboard_1)


@dp.message_handler(Text('Сотрудник (исполнитель)'))
async def worker(message: types.Message):
    deadline = 1
    task = 1
    if task:
        await User.value_2.set()
        await message.answer('Отправьте ссылку на вашего руководителя')
    else:
        await message.answer(f'Ваши задачи до {deadline}: {task}')

a

@dp.message_handler(Text("Менеджер (управляющий)"))
async def lider_name_input(message: types.Message):
    await User.value.set()
    await message.reply('Введите свое ФИО')


@dp.message_handler(state=User.value_2)
async def state_boss(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['value_2'] = message.text
    await state.finish()

    await message.answer(md.bold(data['value_2']))


@dp.message_handler(state=User.value)
async def lider_name_save(message: types.Message, state=FSMContext):
    in_db = True
    connect = True
    async with state.proxy() as data:
        data['value'] = message.text
    await state.finish()

    await message.answer('Проверка в базе...')
    time.sleep(3)
    if in_db and connect:
        await message.answer(md.bold(data['value']))
    elif in_db:
        await message.answer('Ваш менеджер есть в базе, но он вас еще не подключил. ' +
                             'Свяжитесь в вашим менеджером и попросите вас добавить')
    else:
        await message.answer('Ваш менеджер не пользуется данным ботом и отсутствует в базах')


@dp.message_handler(Text('Помощь'))
async def helper(message: types.Message):
    await message.answer('Руководство по боту\n.....')


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
