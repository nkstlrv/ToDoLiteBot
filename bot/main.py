import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import time


# loading local environment variables
load_dotenv()

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher(bot)