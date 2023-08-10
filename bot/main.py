import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from markups import MainMenuMarkup, LoginMarkup, DeleteAccountMarkup
from functions import get_all_users, create_new_user, delete_user
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
    current_user_id = message.from_user.id
    logged_id_users = get_all_users(db)

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

    if current_user_id not in logged_id_users:
        await message.answer("You need to <b>Log-In</b> first", parse_mode="html")
        await message.answer("To <b>login</b>, press 👉 /auth", parse_mode="html")
    else:
        await message.answer(
            "<b>Main Menu</b> ⚙",
            parse_mode="HTML",
            reply_markup=MainMenuMarkup.markup
        )


@dp.message_handler(commands=["menu"])
async def start(message: types.Message):
    current_user_id = message.from_user.id
    logged_id_users = get_all_users(db)

    if current_user_id not in logged_id_users:
        await message.answer("You need to <b>Log-In</b> first", parse_mode="html")
        await message.answer("To <b>login</b>, press 👉 /auth", parse_mode="html")
    else:
        await message.answer("Opening menu", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(
            "<b>Main Menu</b> ⚙",
            parse_mode="HTML",
            reply_markup=MainMenuMarkup.markup,
        )


@dp.message_handler(commands=["auth"])
async def start(message: types.Message):
    current_user_id = message.from_user.id
    logged_id_users = get_all_users(db)

    if current_user_id not in logged_id_users:
        await message.answer(
            "To <b>login</b> press 👇",
            parse_mode="HTML",
            reply_markup=LoginMarkup.markup,
        )
    else:
        await message.answer(
            "To <b>Completely Delete Account</b> press 👇",
            parse_mode="HTML",
            reply_markup=DeleteAccountMarkup.markup,
        )
        await message.answer("Be aware that all your ToDos will be <b>completely deleted</b>", parse_mode="html")


@dp.message_handler(content_types=["text"])
async def menu(message: types.Message):
    current_user = message.from_user.id

    if message.text == "Log-In":

        new_user_id = current_user
        new_user_username = message.from_user.username
        new_user = create_new_user(db, new_user_id, new_user_username)

        if new_user.user_id == current_user:
            await message.answer("You have successfully Logged In",
                                 reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer("Something went wrong")
            await message.answer("Try again", reply_markup=LoginMarkup.markup)

    elif message.text == "Delete my account":

        user_to_delete = current_user
        response = delete_user(db, user_to_delete)

        if response is True:
            await message.answer("You have successfully deleted you account",
                                 reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer("Something went wrong")
            await message.answer("Try again", reply_markup=DeleteAccountMarkup.markup)

    elif message.text == "Abort":
        await message.answer("Aborting", reply_markup=types.ReplyKeyboardRemove())


if __name__ == "__main__":
    logging.info("[STARTING SERVER...]")
    executor.start_polling(dp)
    logging.info("SERVER STOPPED]")
