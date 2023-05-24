from User import *
from buttons import registration, status, main_menu_for_executor, main_menu_for_manager, task_menu_manager, task_menu_executor, executor_menu_manager, manager_menu_executor 
from config import TOKEN
from base.ORM import ManageBot
import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.deep_linking import get_start_link, decode_payload


# Давайте так, если мы создали фунцкию которая не рабочая на 100%, то мы эти строчки просто комментируем


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = ManageBot()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    messages = f"Приветствую тебя, {message.from_user.first_name}. \
                Я Бот Менеджер, и я помогу тебе с твоими делами. \
                В какой сфере ты собираешься использовать бота?"

    if db.check_user(user_name=message.from_user.username) == [] : 
        db.add_user(user_id=message.from_user.id, user_name=message.from_user.username)
        await message.answer(messages, reply_markup=registration)

    elif db.get_state_user(user_id=message.from_user.id) == None:
        await message.answer(messages, reply_markup=registration)

    else:
        state = db.get_state_user(user_id=message.from_user.id)
        if state == True:
            await message.answer("С возвращением!!!", reply_markup=main_menu_for_manager)
        elif state == False:
            await message.answer("С возвращением!!!", reply_markup=main_menu_for_executor)


@dp.message_handler(Text('Бизнес'))
async def busness(message: types.Message):
    await message.reply('Кем ты являешься?', reply_markup=status)
    # await message.reply('Данная функция бота на данный момент находиться в раработке')


# ---------------------------Заполнение информаци о исполнителе------------------------------------
@dp.message_handler(Text('Сотрудник (исполнитель)'))
async def worker(message: types.Message):
    db.add_user_state(user_id=message.from_user.id, state=False)
    await Executor.name.set()
    await message.answer('Введите ваше ФИО')


@dp.message_handler(state=Executor.name)
async def executor_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text

    await Executor.manager.set()
    await msg.answer('Отправьте @username вашего руоводителя в Telegram')


@dp.message_handler(state=Executor.manager)
async def executor_manager(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['manager'] = msg.text

    try:
        manager = md.bold(data['manager'])[1:-1]
        manager_id = db.check_user(user_name=manager)[0][0]
        name = md.bold(data['name'])[1:-1]

        if manager_id:
            db.add_post_to_executors(executor_id=int(msg.from_user.id), name=name, manager_id=manager_id)

            await bot.send_message(chat_id=manager_id, text=f'За вами закрепился новый исполнитель: {name} ({msg.from_user.fullname})')
        else:
            await msg.answer('Данный человек не является пользователем бота. \
                            Проверьте правильность введенного имени или попросите его воспользоваться ботом')
    except:
        await msg.answer('Что-то пошло не так. Проверьте правильность введенных данных или попробуйте позже')


# ------------------------Заполнение данных о менеджере---------------------------
@dp.message_handler(Text("Менеджер (управляющий)"))
async def lider_name_input(message: types.Message):
    db.add_user_state(user_id=message.from_user.id, state=True)

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


# ----------------------------------------menu executor----------------------------------------------
@dp.message_handler(Text('Мои задачи'))
async def my_task(message: types.Message):
    ts = db.get_task(executor_id=message.from_user.id)
    if ts != None:
        await message.answer(f'Задача для тебя: \nЗадача: {ts[0][0]}\n{ts[0][1]}\nВремя выполнения: {ts[0][2]} часов', reply_markup=task_menu_executor)
    else:
        await message.answer('У тебя нет активных задач')


@dp.message_handler(Text('Подтверить выполнение задачи'))
async def sucs_task(message: types.Message):
    db.complete_tasks(user_id=message.from_user.id)

    manager = db.get_manager_for_executor(executor_id=message.from_user.id)[0][1]
    db.complete_tasks(user_id=message.from_user.id)
    await bot.send_message(manager, f'@{message.from_user.username} успешно выполнил задачу')

    await message.answer('Поздравляю в выполнениой задачей', reply_markup=main_menu_for_executor)


@dp.message_handler(Text('Менеджеры'))
async def get_my_manager(message: types.Message):
    my_manager = db.get_manager_for_executor(executor_id=message.from_user.id)[0][1]
    my_manager = db.get_username(user_id=message.from_user.id)
    await message.answer(f'Tвой менеджер: @{my_manager}',reply_markup=executor_menu_manager)
# ---------------------------------------------------------------------------------------------------------


# -----------------------------------Menu manager --------------------------------------------------------
@dp.message_handler(Text('Задачи'))
async def task_man(message: types.Message):
    e_id = db.get_executor_for_manager(manager_id=message.from_user.id)
    ts = db.get_task(executor_id=e_id)

    if ts != []:
        await message.answer(f"Вот задача, которую вы установили своему исполнителю: Задача: {ts[0][0]}\n{ts[0][0]}\nВремя выполнения: {ts[0][0]} часов", reply_markup=task_menu_manager)
    else:
        await message.answer('На данный момент нет активной задачи', reply_markup=task_menu_manager)


@dp.message_handler(Text('Добавить задачу'))
async def set_task(message: types.Message):
    await Task.name.set()
    await message.reply('Введите название задачи')


@dp.message_handler(state=Task.name)
async def task_set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Task.description.set()
    await message.reply('Введите описание к задаче')


@dp.message_handler(state=Task.description)
async def task_set_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['decription'] = message.text

    await Task.time.set()
    await message.reply('Введите количество часов на выполнение задачи\nМинимальное значение: 1')


@dp.message_handler(state=Task.time)
async def task_set_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text

    name = md.bold(data['name'])[1:-1]
    descr = md.bold(data['decription'])[1:-1]
    time = md.bold(data['time'])[1:-1]

    await state.finish()

    e_id = db.get_executor_for_manager(manager_id=message.from_user.id)
    db.add_new_task(task_name=name, task=descr, date=time, executor_id=e_id)
    await bot.send_message(e_id, f"Поставлена новая задача!!!\nЗадача: {name}\n{descr}\nВремя выполнения (часов): {time}")
    await message.answer(f'Ваша задача успешно установленна.\nЗадача: {name}\nВремя выполнения (часов): {time}')

# ---------------------------------------------------------------------------------------------------------

@dp.message_handler(Text('Hазад'))
async def back(message: types.Message):
    state = db.get_state_user(user_id=message.from_user.id)
    if state == True:
        await message.answer("Главное меню", reply_markup=main_menu_for_manager)
    elif state == False:
        await message.answer("Главное меню", reply_markup=main_menu_for_executor)


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
