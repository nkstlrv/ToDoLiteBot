from aiogram import types


class MainMenuMarkup:
    b1 = types.KeyboardButton("Add new task")
    b2 = types.KeyboardButton("Show all tasks")
    b3 = types.KeyboardButton("Delete task")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(b1, b2, b3)





