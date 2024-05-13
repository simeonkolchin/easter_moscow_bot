from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.types import Message

import config
import sqlite_db
from handlers import keyboards

router = Router()


class admin_state(StatesGroup):
    create_admin = State()

    send_massage_all = State()
    send_photo_all = State()
    send_massage_all_clear = State()


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
    admins = [int(i[1]) for i in admins]
    if int(message.chat.id) in admins:
        await sqlite_db.get_people()
        from aiogram.types import FSInputFile
        file = FSInputFile("people.xlsx")
        await message.answer_document(file)


@router.message(Command("send_invoice_2024"))
async def admin_call_people_(message: Message, state: FSMContext, bot: Bot):
    admins = await sqlite_db.get_admins()
    admins = [i[1] for i in admins]
    if message.chat.id in admins:
        await message.answer_photo(photo=FSInputFile('files/style.webp'), caption="Отправьте мне текст для всех пользователей:")
        await state.set_state(admin_state.send_massage_all)
        await state.update_data(photo=0)


@router.message(admin_state.send_massage_all)
async def send_massage_all(message: Message, state: FSMContext, bot: Bot):
    text = message.text
    await state.update_data(text=text)
    data = await state.get_data()
    if data['photo']:
        await message.answer_photo(photo=FSInputFile('files/send_photo_invoice.jpg'), caption=f"{data['text']}"
                             f"\n\nВот ваш текст c картинкой. Выберите опцию:",
                             reply_markup=keyboards.send_invoice_edit_photo().as_markup())
    else:
        await message.answer(f"{data['text']}"
                         f"\n\nВот ваш текст. Выберите опцию:", reply_markup=keyboards.send_invoice_edit_text().as_markup())
    await state.set_state(admin_state.send_massage_all_clear)


@router.callback_query(F.data == "send_invoice_add_photo")
async def send_invoice_add_photo(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['photo']:
        await callback.message.edit_caption(caption=f"Текущее фото ☝️"
                                                    f"\n\nОтправьте мне новую фотографию:")
    else:
        await callback.message.edit_text(f"Отправьте мне фотографию:")
    await state.set_state(admin_state.send_photo_all)


@router.message(admin_state.send_photo_all)
async def send_photo_all(message: Message, state: FSMContext, bot: Bot):
    await message.bot.download(file=message.photo[-1].file_id, destination='files/send_photo_invoice.jpg')
    await state.update_data(photo=1)
    data = await state.get_data()
    if data['photo']:
        await message.answer_photo(photo=FSInputFile('files/send_photo_invoice.jpg'), caption=f"{data['text']}"
                             f"\n\nВот ваш текст c картинкой. Выберите опцию:",
                             reply_markup=keyboards.send_invoice_edit_photo().as_markup())
    else:
        await message.answer(f"{data['text']}"
                         f"\n\nВот ваш текст. Выберите опцию:", reply_markup=keyboards.send_invoice_edit_text().as_markup())
    await state.set_state(admin_state.send_massage_all_clear)


@router.callback_query(F.data == "send_invoice_edit_text")
async def send_invoice_edit_text(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['photo']:
        await callback.message.edit_caption(caption=f"Текущий текст:"
                                         f"\n\n{data['text']}"
                                         f"\n\nОтправьте мне новый текст:")
    else:
        await callback.message.edit_text(f"Текущий текст:"
                                         f"\n\n{data['text']}"
                                         f"\n\nОтправьте мне новый текст:")
    await state.set_state(admin_state.send_massage_all)


@router.callback_query(F.data == "send_invoice_send_message")
async def send_invoice_send_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    admins = await sqlite_db.get_admins()
    admins = [i[1] for i in admins]
    if callback.message.chat.id in admins:
        data = await state.get_data()
        if data['photo']:
            await callback.message.edit_caption(caption=data['text'])
        else:
            await callback.message.edit_text(data['text'])
        users = await sqlite_db.get_users()
        for user in users:
            try:
                if data['photo']:
                    await bot.send_photo(int(user[2]), photo=FSInputFile('files/send_photo_invoice.jpg'), caption=data['text'])
                else:
                    await bot.send_message(int(user[2]), data['text'])
            except:
                continue
        await callback.message.answer(f"Сообщение отправлено!")
        await state.clear()


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
