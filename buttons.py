from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup()
buts = ['Бизнес', "Семья"]
but1 = KeyboardButton('Для себя')
helps = KeyboardButton('Помощь')
keyboard.add(*buts).add(but1).add(helps)

keyboard_1 = ReplyKeyboardMarkup()
buts_1 = ['Сотрудник (исполнитель)', "Менеджер (управляющий)"]
keyboard_1.add(*buts_1)

keyb = ReplyKeyboardMarkup()
b1 = KeyboardButton('13-15')
b2 = KeyboardButton('16-18')
b3 = KeyboardButton('18+')
keyb.add(b1).add(b2).add(b3)

keyb2 = ReplyKeyboardMarkup()
b4 = KeyboardButton('Суши')
b5 = KeyboardButton('Пицца')
b6 = KeyboardButton('Вок')
keyb2.add(b4).add(b5).add(b6)

keyb3 = ReplyKeyboardMarkup()
b7 = KeyboardButton('Ужасы')
b8 = KeyboardButton('Драмма')
b9 = KeyboardButton('Комедия')
keyb3.add(b7).add(b8).add(b9)
