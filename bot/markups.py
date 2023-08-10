from aiogram import types


class MainMenuMarkup:
    b1 = types.KeyboardButton("/add_task")
    b2 = types.KeyboardButton("/show_tasks")
    b3 = types.KeyboardButton("/show_completed_tasks")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(b1, b2, b3)


abort_btn = types.KeyboardButton("Abort")


class LoginMarkup:
    login_btn = types.KeyboardButton("Log-In")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(login_btn, abort_btn)


class DeleteAccountMarkup:
    btn = types.KeyboardButton("Delete my account")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn, abort_btn)
