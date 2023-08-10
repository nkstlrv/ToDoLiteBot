from aiogram import types


class MainMenuMarkup:
    b1 = types.KeyboardButton("📝 Add new task")
    b2 = types.KeyboardButton("📑 Show all tasks")
    b3 = types.KeyboardButton("✅ Complete task")
    b4 = types.KeyboardButton("❌ Clear completed tasks")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(b1, b2, b3, b4)





