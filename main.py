import time
from buttons import *
from config import TOKEN
from base.ORM import ManageBot
import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from User import *
import re

# Давайте так, если мы создали фунцкию которая не рабочая на 100%, то мы эти строчки просто комментируем

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = ManageBot()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # TODO: save to database message.user_id, message.username
    db.add_user(user_id=message.from_user.id, user_name=message.from_user.full_name)
    await message.answer(f"Приветствую тебя, {message.from_user.first_name}. " +
                        "Я Бот Менеджер, и я помогу тебе с твоими делами. " +
                        "В какой сфере ты собираешься использовать бота?", reply_markup=keyboard)


@dp.message_handler(Text('Бизнес'))
async def busness(message: types.Message):
    await message.reply('Кем ты являешься?', reply_markup=keyboard_1)
    # await message.reply('Данная функция бота на данный момент находиться в раработке')

# ---------------------------Заполнение информаци о исполнителе------------------------------------
@dp.message_handler(Text('Сотрудник (исполнитель)'))
async def worker(message: types.Message):
    await Executor.name.set()
    await message.answer('Введите ваше ФИО')


@dp.message_handler(state=Executor.name)
async def executor_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text

    await Executor.manager.set()
    await msg.answer('Отправьте полное имя вашего руоводителя в Telegram')


@dp.message_handler(state=Executor.manager)
async def executor_manager(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['manager'] = msg.text

    try:
        manager = md.bold(data['manager'])[1:-1]
        manager_id = db.check_user(user_name=manager)[0][0]
        name = md.bold(data['name'])[1:-1]

        db.add_post_to_executors(executor_id=int(msg.from_user.id), name=name, manager_id=manager_id)
    except:
        await msg.answer('Данный человек не является пользователем бота. \
                        Проверьте правильность введенного имени или попросите его воспользоваться ботом')


# ------------------------Заполнение данных о менеджере---------------------------
@dp.message_handler(Text("Менеджер (управляющий)"))
async def lider_name_input(message: types.Message):
    await Manager.name.set()
    await message.reply('Введите свое ФИО')


@dp.message_handler(state=Manager.name)
async def state_boss(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Manager.executor.set()
    await message.answer(md.bold(data['name']))
    await message.answer('Отправьте ссылку на вашего работника')


@dp.message_handler(state=Manager.executor)
async def lider_name_save(message: types.Message, state=FSMContext):
    in_db = True
    connect = True
    async with state.proxy() as data:
        data['executor'] = message.text
    await state.finish()

    await message.answer('Проверка в базе...')
    time.sleep(3)
    if in_db and connect:
        await message.answer(md.bold(data['worker']))
    elif in_db:
        await message.answer('Ваш менеджер есть в базе, но он вас еще не подключил. ' +
                            ' Свяжитесь в вашим менеджером и попросите вас добавить')
    else:
        await message.answer('Ваш менеджер не пользуется данным ботом и отсутствует в базах')
# -------------------------------------------------------------------------------

# ------------------------------- Family ----------------------------------------
@dp.message_handler(Text('Семья'))
async def family(message: types.Message):
    # await message.reply('Кем ты являешься?', reply_markup=keyboard_1)
    await message.reply('Данная функция бота на данный момент находиться в раработке')
# -------------------------------------------------------------------------------

# -------------------------------- For me ---------------------------------------
@dp.message_handler(Text('Для себя'))
async def for_me(message: types.Message):
    await Formyself.name.set()
    await message.reply('Введите название задачи')


@dp.message_handler(state=Formyself.name)
async def for_me_set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Formyself.description.set()
    await message.reply('Введите описание к задаче')


@dp.message_handler(state=Formyself.description)
async def for_me_set_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['decription'] = message.text

    await Formyself.time.set()
    await message.reply('Введите количество часов на выполнение задачи\nМинимальное значение: 1')


@dp.message_handler(state=Formyself.time)
async def for_me_set_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text

    name = md.bold(data['name'])[1:-1]
    time = md.bold(data['time'])[1:-1]

    await state.finish()
    await message.answer(f'Ваша задача успешно установленна.\nЗадача: {name}\nВремя выполнения (часов): {time}')
# -------------------------------------------------------------------------------


@dp.message_handler(Text('Помощь'))
async def helper(message: types.Message):
    await message.answer('Руководство по боту\n')


# @dp.message_handler(Text('Семья'))
# async def family(message: types.Message):
#     await User.family.set()
#     await message.reply("Введите своё ФИО, и кем вы являетесь через дефис, например:\nНиколай Николаевич - Старший сын")


# @dp.message_handler(state=User.family)
# async def state_family(message: types.Message, state=FSMContext):
#     name = message.text.split(sep=" - ", maxsplit=1)
#     async with state.proxy() as data:
#         data['family'] = message.text
#     await state.finish()
#     await message.answer(md.bold(data['family']))
#     await message.answer("Добавьте в свою семью пользователей, или всупити уже в существующую!", reply_markup=keyboard_fam)


# @dp.message_handler(Text('Добавить участников'))
# # Придумать способ добавления
# async def add_peoples(message: types.message):
#     ...


# @dp.message_handler(commands=["ref"])
# async def get_ref(message: types.Message):
#     link = await get_start_link(str(message.from_user.username), encode=True)
#     # result: 'https://t.me/MyBot?start='
#     # после знака = будет закодированный никнейм юзера, который создал реф ссылку, вместо него можно вставить и его id 
#     await message.answer(f"Ваша реф. ссылка {link}")


# # хендлер для расшифровки ссылки
# @dp.message_handler(commands=["start"])
# async def handler(message: types.Message):
#     args = message.get_args()
#     reference = decode_payload(args)
#     await message.answer(f"Ваш реферал {reference}")


# @dp.message_handler(Text("Присоедениться"))
# # Придумать способ присоединения, скорее всего через машину состояний или не знаю как...
# async def join_family(message: types.Message):
#     ...


# @dp.message_handler(Text('Для себя'))
# async def for_self(message: types.Message):
#     await User.self.set()
#     await message.reply("Введите своё ФИО")


# @dp.message_handler(state=User.self)
# async def save_self(message: types.Message, state=FSMContext):
#     async with state.proxy() as data:
#         data['self'] = message.text
#     await state.finish()
#     await message.answer(md.bold(data['self']))


# @dp.message_handler(commands="set task")
# # придумать способ отслеживания списка участников, добавления их в кнопки и отслеживание выбранного участника
# async def set_task(message: types.Message):
#     await message.answer("Для кого задание?", reply_markup=keyboard_task)



@dp.message_handler(content_types=['any'])
async def nonetype_message(message: types.Message):
    await message.reply('Я не понимаю что ты от меня хочешь 😅')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
