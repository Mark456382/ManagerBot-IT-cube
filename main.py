from config import TOKEN
from buttons import *
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text


bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(f"Приветствую тебя, {message.from_user.first_name}. "+
                         "Я Бот Менеджер, и я помогу тебе с твоими делами. "+
                         "В какой сфере ты собираешься использовать бота?", reply_markup=keyboard)


@dp.message_handler(Text('Бизнес'))
async def busness(message: types.Message):
    await message.reply('Кем ты являешься?', reply_markup=keyboard_1)


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
