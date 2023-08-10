import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from markups import MainMenuMarkup
from db_functions import (
    get_all_users, create_new_user,
    delete_user, get_all_user_tasks,
    create_task, get_all_user_todo_tasks,
    mark_task_done, get_all_user_done_tasks,
    delete_completed_tasks

)
import time
import logging
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
    if "%new" in message.text:
        task = message.text.split('%new')[-1].strip()
        if task.strip() != "":
            response = create_task(db, task, current_user.id)
            if response:
                await message.answer("New task created")
                await message.answer(response.name)
            else:
                await message.answer("This task already exists")

    elif "%complete" in message.text:
        task_to_complete = message.text.split('%complete')[-1].strip()

        if task_to_complete.strip() != "":
            todo_tasks: list = get_all_user_todo_tasks(db, message.from_user.id)
            tasks_dict = dict()
            for ind, task in enumerate(todo_tasks, start=1):
                tasks_dict[ind] = task.task_id

            task_to_complete = int(task_to_complete)

            response = mark_task_done(db, tasks_dict[task_to_complete])
            if response:
                await message.answer("Marked as completed")
            else:
                await message.answer("This task is already completed")

    elif "%clear" in message.text:
        delete_completed_tasks(db, current_user.id)
        await message.answer("Cleared all completed tasks")

    # Buttons handling
    if message.text == "📝 Add new task":
        await message.answer("To add new Task use format:")
        await message.answer("<b><i>%new Go shopping</i></b>", parse_mode="html")
    elif message.text == "📑 Show all tasks":

        all_tasks = get_all_user_tasks(db, message.from_user.id)

        if all_tasks:

            done_dict = {True: "✅", False: " 🔘"}
            msg = str()

            for task in all_tasks:
                msg += f"\n{task.name} {done_dict[task.done]}\n"

            await message.answer("Here are your tasks:")
            await message.answer(msg)

        else:
            await message.answer("Your ToDo list is empty")

    elif message.text == "✅ Complete task":

        todo_tasks: list = get_all_user_todo_tasks(db, message.from_user.id)

        msg = str()
        tasks_dict = dict()

        for ind, task in enumerate(todo_tasks, start=1):
            msg += f"\n{ind}) {task.name}  🔘\n"
            tasks_dict[ind] = task.task_id

        if todo_tasks:
            await message.answer("Here are your ToDo tasks")
            await message.answer(msg)
            time.sleep(1)
            await message.answer("To mark task as Done type: <b><i>%complete id</i></b>",
                                 parse_mode="html")
            await message.answer("For example: \n\n"
                                 "1) Task 1  🔘\n"
                                 "2) Task 2  🔘\n\n"
                                 "%complete 2", parse_mode="html")
        else:
            await message.answer("Your ToDo list is empty")

    elif message.text == "❌ Clear completed tasks":

        completed_tasks = get_all_user_done_tasks(db, message.from_user.id)
        if completed_tasks:
            msg = str()
            for task in completed_tasks:
                msg += f"\n{task.name}  ✅\n"
            await message.answer("Here are your completed tasks")
            await message.answer(msg)
            time.sleep(1)
            await message.answer("If you want to delete all you completed tasks, type: \n\n"
                                 "<b><i>%clear</i></b>", parse_mode="html")
        else:
            await message.answer("Your do not have completed tasks")


@dp.message_handler(commands=["delete"])
async def delete(message: types.Message):
    current_user = message.from_user.id
    delete_user(db, current_user)
    await message.answer("All your task have been deleted", reply_markup=types.ReplyKeyboardRemove())


if __name__ == "__main__":
    executor.start_polling(dp)
