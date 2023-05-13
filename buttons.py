from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup()
buts = ['Бизнес', "Семья"]
but1 = KeyboardButton('Для себя')
helps = KeyboardButton('Помощь')
keyboard.add(*buts).add(but1).add(helps)

keyboard_1 = ReplyKeyboardMarkup()
buts_1 = ['Сотрудник (исполнитель)', "Менеджер (управляющий)"]
keyboard_1.add(*buts_1)

keyboard_task = ReplyKeyboardMarkup()
peoples = ["Для себя"]
keyboard_task.add(*peoples)

# keyboard_fam = ReplyKeyboardMarkup
# buttons = ['Добавить участников', "Присоедениться"]
# keyboard_fam.add(*buttons)

