import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from markups import MainMenuMarkup
from db_functions import (
    get_all_users, create_new_user,
    delete_user, get_all_user_tasks,
    create_task, get_all_user_done_tasks

)
import time
import logging
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

# loading local environment variables
load_dotenv()

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    current_user = message.from_user
    logged_id_users = get_all_users(db)

    # Adding User to DB if not signed-up
    if current_user not in logged_id_users:
        create_new_user(db, user_id=current_user.id, username=current_user.username)

    await message.answer(
        f"Hello there, <i><b>{message.chat.first_name}</b></i> 👋",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    time.sleep(1)
    await message.answer("This is <b>ToDoLite</b> bot 🤖", parse_mode="HTML")
    await message.answer(
        "I can help you with your ToDo tasks",
        parse_mode="HTML",
        reply_markup=MainMenuMarkup.markup
    )
    time.sleep(1)


@dp.message_handler(content_types=["text"])
async def todo_menu(message: types.Message):
    current_user = message.from_user

    # User Reply handling
    if "@new" in message.text:
        task = message.text.split('@new')[-1].strip()
        if task.strip() != "":
            response = create_task(db, task, current_user.id)
            if response:
                await message.answer("New task created")
            else:
                await message.answer("This task already exists")

    # Buttons handling
    if message.text == "📝 Add new task":
        await message.answer("To add new Task use format:")
        await message.answer("<b><i>@new Go shopping</i></b>", parse_mode="html")
    elif message.text == "📑 Show all tasks":

        all_tasks = get_all_user_tasks(db, message.from_user.id)
        print(all_tasks)
        if all_tasks:
            await message.answer("Here are your tasks")
        else:
            await message.answer("Your ToDo list is empty")

    elif message.text == "❌ Delete task":

        all_tasks = get_all_user_tasks(db, message.from_user.id)
        if all_tasks:
            await message.answer("Here are your tasks")
        else:
            await message.answer("Your ToDo list is empty")


@dp.message_handler(commands=["delete"])
async def delete(message: types.Message):
    current_user = message.from_user.id
    delete_user(db, current_user)
    await message.answer("All your task have been deleted", reply_markup=types.ReplyKeyboardRemove())


if __name__ == "__main__":
    executor.start_polling(dp)
