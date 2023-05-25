from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# -----------------------------Регистрация-------------------------------
registration = ReplyKeyboardMarkup(resize_keyboard=True)
spetiality = ['Бизнес', "Семья"]
spetiality_1 = KeyboardButton('Для себя')
helps = KeyboardButton('Помощь')
registration.add(*spetiality).add(spetiality_1).add(helps)

status = ReplyKeyboardMarkup(resize_keyboard=True)
status_val = ['Сотрудник (исполнитель)', "Менеджер (управляющий)"]
status.add(*status_val)

info = KeyboardButton('О Боте')
# ------------------------------------------------------------

# ------------------------------Панель менеджера------------------------------
main_menu_for_manager = ReplyKeyboardMarkup(resize_keyboard=True)
menu_m = ['Задачи', 'Сотрудники']
main_menu_for_manager.add(*menu_m).add(info)

back = KeyboardButton('Hазад')

task_menu_manager = ReplyKeyboardMarkup(resize_keyboard=True)
add_task = KeyboardButton('Добавить задачу')
task_menu_manager.add(add_task).add(back)


manager_menu_executor = ReplyKeyboardMarkup(resize_keyboard=True)
add_executor = KeyboardButton('Сменить исполнителя')
manager_menu_executor.add(add_executor).add(back)
# ------------------------------------------------------------


# ------------------------------Панель исполнителя------------------------------
main_menu_for_executor = ReplyKeyboardMarkup(resize_keyboard=True)

menu_e = ['Мои задачи', 'Менеджеры']
main_menu_for_executor.add(*menu_e).add(info)

task_menu_executor = ReplyKeyboardMarkup(resize_keyboard=True)
sucs_task = KeyboardButton('Подтверить выполнение задачи')
task_menu_executor.add(sucs_task).add(back)

executor_menu_manager = ReplyKeyboardMarkup(resize_keyboard=True)
add_manager = KeyboardButton('Добавить менеджера')
delete_manager = KeyboardButton('Отвязаться от менеджера')
executor_menu_manager.add(add_manager).add(delete_manager).add(back)
# ------------------------------------------------------------
# keyboard_fam = ReplyKeyboardMarkup
# buttons = ['Добавить участников', "Присоедениться"]
# keyboard_fam.add(*buttons)

