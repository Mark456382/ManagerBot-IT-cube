import time

import User

from buttons import *
from config import TOKEN
import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from User import *

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


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
    deadline = 0
    task = 0
    if task:
        await User.employer.set()
        await message.answer('Отправьте ссылку на вашего руководителя')
    else:
        await message.answer(f'Ваши задачи до {deadline}: {task}')


@dp.message_handler(Text("Менеджер (управляющий)"))
async def lider_name_input(message: types.Message):
    await User.worker.set()
    await message.reply('Введите свое ФИО')


@dp.message_handler(state=User.employer)
async def state_boss(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['employer'] = message.text
    await state.finish()
    await message.answer(md.bold(data['employer']))


@dp.message_handler(state=User.worker)
async def lider_name_save(message: types.Message, state=FSMContext):
    in_db = True
    connect = True
    async with state.proxy() as data:
        data['worker'] = message.text
    await state.finish()

    await message.answer('Проверка в базе...')
    time.sleep(3)
    if in_db and connect:
        await message.answer(md.bold(data['worker']))
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
    await User.family.set()
    await message.reply("Введите своё ФИО, и кем вы являетесь через дефис, например:\nНиколай Николаевич - Старший сын")


@dp.message_handler(state=User.family)
async def state_family(message: types.Message, state=FSMContext):
    name = message.text.split(sep=" - ", maxsplit=1)
    async with state.proxy() as data:
        data['family'] = message.text
    await state.finish()
    await message.answer(md.bold(data['family']))
    await message.answer("Добавьте в свою семью пользователей, или всупити уже в существующую!", reply_markup=keyboard_fam)


@dp.message_handler(Text('Добавить участников'))
# Придумать способ добавления
async def add_peoples(message: types.message):
    ...

@dp.message_handler(Text("Присоедениться"))
# Придумать способ присоединения, скорее всего через машину состояний или не знаю как...
async def join_family(message: types.Message):
    ...


@dp.message_handler(Text('Для себя'))
async def for_self(message: types.Message):
    await User.self.set()
    await message.reply("Введите своё ФИО")


@dp.message_handler(state=User.self)
async def save_self(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['self'] = message.text
    await state.finish()
    await message.answer(md.bold(data['self']))


@dp.message_handler(commands="set task")
# придумать способ отслеживания списка участников, добавления их в кнопки и отслеживание выбранного участника
async def set_task(message: types.Message):
    await message.answer("Для кого задание?", reply_markup=keyboard_task)



@dp.message_handler(content_types=['any'])
async def nonetype_message(message: types.Message):
    await message.reply('Я не понимаю что ты от меня хочешь 😅')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
