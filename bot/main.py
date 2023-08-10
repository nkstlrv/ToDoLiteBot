import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from markups import MainMenuMarkup
from functions import get_all_users, create_new_user, delete_user, create_task
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

# Argument needed to understand weather to process user inputs
do_receive_messages = False


def make_do_receive_true():
    global do_receive_messages
    do_receive_messages = True


def make_do_receive_false():
    global do_receive_messages
    do_receive_messages = False


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
    )
    time.sleep(1)


if __name__ == "__main__":
    executor.start_polling(dp)
