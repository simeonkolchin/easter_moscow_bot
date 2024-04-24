from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

import config
import sqlite_db

router = Router()


class admin_state(StatesGroup):
    create_admin = State()


@router.message(Command("admin"))
async def admin_page(message: Message, state: FSMContext):
    admins = await sqlite_db.get_admins()
    admins = [i[1] for i in admins]
    if message.chat.id in admins:
        await message.answer(f"Отправьте мне id пользователя (Чтобы узнать id, напишите /my_id):")
        await state.set_state(admin_state.create_admin)


@router.message(Command("get_people"))
async def admin_call_people_(message: Message, state: FSMContext):
    admins = await sqlite_db.get_admins()
    admins = [i[1] for i in admins]
    if message.chat.id in admins:
        await sqlite_db.get_people()
        from aiogram.types import FSInputFile
        file = FSInputFile("event_people.xlsx")
        await message.answer_document(file, caption="Вот список тех, кто зарегистрировался в боте:")

@router.message(admin_state.create_admin)
async def create_admin(message: Message, state: FSMContext):
    admin_id = message.text
    users = await sqlite_db.get_users()
    users_ids = [i[2] for i in users]
    if int(admin_id) in users_ids:
        await sqlite_db.create_admin(int(admin_id))
        await message.answer(f"Добавлен новый администратор")
        await state.clear()
    else:
        await message.answer(
            f"Пользователя нет в моей базе данных! Сначала человеку с id: {admin_id} нужно пройти регистрацию в боте, "
            f"а потом вы можете сделать его администратором. Отправьте мне id пользователя (Чтобы узнать id, напишите /my_id):")
        await state.set_state(admin_state.create_admin)


@router.message(Command("create_admin"))
async def admin_page(message: Message):
    if message.chat.id in config.admins:
        await sqlite_db.create_admin(message.chat.id)
        print('Вы администратор')
        await message.answer(f"Вы администратор")
