from aiogram import types


class MainMenuMarkup:
    b1 = types.InlineKeyboardButton("Add Task", callback_data="task_add")
    b2 = types.InlineKeyboardButton("My ToDos", callback_data="tasks_show")
    b3 = types.InlineKeyboardButton("Completed tasks", callback_data="tasks_show_done")
    # b4 = types.InlineKeyboardButton("Mark as done", callback_data="tasks_mark_as_done")
    # b5 = types.InlineKeyboardButton("Delete task", callback_data="tasks_delete")
    markup = types.InlineKeyboardMarkup(resize_keyboard=True).add(b1, b2, b3)


class LoginMarkup:
    login_btn = types.KeyboardButton("Log-In")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(login_btn)