import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import time
import logging
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

# loading local environment variables
load_dotenv()

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher(bot)

dp.message_handler(commands=["start"])


async def start(message: types.Message):
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
    await message.answer(
        "<b>Main Menu</b> ⚙",
        parse_mode="HTML",
    )


if __name__ == "__main__":
    logging.info("[STARTING SERVER...]")
    executor.start_polling(dp)
    logging.info("SERVER STOPPED]")
