from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.types import Message
from handlers import keyboards
import sqlite_db
from files import questions as q
import time
from files import texts
import random

router = Router()


class main_state(StatesGroup):
    get_person_name = State()

    help = State()

    ask_a_question = State()

    answer_help = State()


@router.message(Command("start"))
async def start(message: Message, bot: Bot):
    users = await sqlite_db.get_users()
    user = True if message.chat.id in [i[2] for i in users] else False
    if not user:
        video_path = 'files/easter.mp4'
        video_file = FSInputFile(video_path)
        video_width = 1280
        video_height = 720
        await message.answer(f"Привет, {message.from_user.first_name}" + texts.text_1)
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        await bot.send_video(chat_id=message.chat.id, video=video_file, width=video_width, height=video_height)
        time.sleep(10)
        await message.answer(texts.text_2, reply_markup=keyboards.whathappenthere().as_markup())
        time.sleep(10)
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        media = [InputMediaPhoto(media=FSInputFile('files/1.jpg'), caption=texts.text_3)]
        media.append(InputMediaPhoto(media=FSInputFile('files/2.jpg')))
        media.append(InputMediaPhoto(media=FSInputFile('files/3.jpg')))
        media.append(InputMediaPhoto(media=FSInputFile('files/4.jpg')))
        media.append(InputMediaPhoto(media=FSInputFile('files/5.jpg')))
        media.append(InputMediaPhoto(media=FSInputFile('files/6.jpg')))
        await message.answer_media_group(media=media)
        time.sleep(10)
        await message.answer(texts.text_5, reply_markup=keyboards.text_5().as_markup())
        time.sleep(4)
        await message.answer(texts.text_6,
                                      reply_markup=keyboards.get_start_keyboard().as_markup())
        await sqlite_db.push_data_in_people(message.from_user.first_name, message.chat.id)
    else:
        await message.answer(f"{message.from_user.first_name}, чем я могу тебе помочь?",
                             reply_markup=keyboards.get_start_keyboard().as_markup())


@router.callback_query(F.data == "start")
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(texts.text_6, reply_markup=keyboards.get_start_keyboard().as_markup())
    await state.clear()


# @router.callback_query(F.data == "whathappenthere")
# async def whathappenthere(callback: types.CallbackQuery, bot: Bot):
#     await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
#     media = [InputMediaPhoto(media=FSInputFile('files/1.jpg'), caption=texts.text_3)]
#     media.append(InputMediaPhoto(media=FSInputFile('files/2.jpg')))
#     media.append(InputMediaPhoto(media=FSInputFile('files/3.jpg')))
#     media.append(InputMediaPhoto(media=FSInputFile('files/4.jpg')))
#     media.append(InputMediaPhoto(media=FSInputFile('files/5.jpg')))
#     media.append(InputMediaPhoto(media=FSInputFile('files/6.jpg')))
#     await callback.message.answer_media_group(media=media)
#     time.sleep(10)
#     await callback.message.answer(texts.text_5, reply_markup=keyboards.text_5().as_markup())
#     time.sleep(4)
#
#     await callback.message.answer(texts.text_6,
#                                   reply_markup=keyboards.get_start_keyboard().as_markup())
#     await sqlite_db.push_data_in_people(callback.from_user.first_name, callback.message.chat.id)


@router.callback_query(F.data.startswith("question_"))
async def event_(callback: types.CallbackQuery):
    question_number = callback.data.split("_")[1]
    await callback.message.edit_text(f"{q.answers[int(question_number)]}",
                                     reply_markup=keyboards.questions().as_markup())


@router.callback_query(F.data.startswith("add_calendar"))
async def event_(callback: types.CallbackQuery):
    await callback.message.edit_text("Теперь твой календарь на стороне Пасхи!",
                                     reply_markup=keyboards.calendar().as_markup())


@router.callback_query(F.data.startswith("information_easter_1"))
async def information_easter_1(callback: types.CallbackQuery):
    await callback.message.edit_text(texts.text_7,
                                     reply_markup=keyboards.information_easter_1().as_markup())


@router.callback_query(F.data.startswith("information_easter_2"))
async def information_easter_2(callback: types.CallbackQuery):
    await callback.message.edit_text(texts.text_8,
                                     reply_markup=keyboards.information_easter_2().as_markup())


@router.callback_query(F.data.startswith("information_easter_3"))
async def information_easter_3(callback: types.CallbackQuery):
    await callback.message.edit_text(texts.text_9,
                                     reply_markup=keyboards.information_easter_3().as_markup())


@router.callback_query(F.data.startswith("information_event"))
async def event_(callback: types.CallbackQuery):
    await callback.message.edit_text(texts.text_10,
                                     reply_markup=keyboards.information_event().as_markup())


@router.callback_query(F.data.startswith("information_create"))
async def event_(callback: types.CallbackQuery):
    await callback.message.edit_text(texts.text_11,
                                     reply_markup=keyboards.information_create().as_markup())


@router.callback_query(F.data.startswith("get_gift"))
async def event_(callback: types.CallbackQuery):
    await callback.message.edit_text(texts.text_12,
                                     reply_markup=keyboards.get_gift().as_markup())


@router.callback_query(F.data == "ask_a_question")
async def ask_a_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"Выбери один из распространенных вопросов или задай свой:\n",
                                     reply_markup=keyboards.help_callback().as_markup())
    await state.clear()


@router.callback_query(F.data == "cin_question")
async def cin_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"Напиши свой вопрос:\n",
                                     reply_markup=keyboards.cin_question().as_markup())
    await state.set_state(main_state.ask_a_question)


@router.message(main_state.ask_a_question)
async def ask_a_question_(message: Message, state: FSMContext, bot: Bot):
    text = message.text
    await bot.send_message(-1002017715249, f"<b>Вопрос?</b>\n"
                                           f"<code>id: {message.chat.id}</code> | @{message.from_user.username}\n\n"
                                           f"{text}", reply_markup=keyboards.reply_help(message.chat.id).as_markup())
    await message.answer(f"Спасибо за твой вопрос!🤗 Я уже передал его моим создателям. Скоро вернусь с ответом",
                         reply_markup=keyboards.help_router().as_markup())
    await state.clear()


@router.callback_query(F.data.startswith("reply_help_"))
async def reply_help(callback: types.CallbackQuery, state: FSMContext):
    help_message_id = callback.data.split("_")[2]
    await state.update_data(help_message_id=help_message_id)
    await callback.message.answer(f"Напишите ответ на сообщение:")
    await state.set_state(main_state.answer_help)


@router.message(main_state.answer_help)
async def answer_help(message: Message, state: FSMContext, bot: Bot):
    answer_text = message.text
    data = await state.get_data()
    await bot.send_message(chat_id=int(data['help_message_id']), text=answer_text)
    await message.answer(f"Сообщение отправлено!")
    await state.clear()


@router.message(Command("id"))
async def start(message: Message):
    await message.answer(f"{message.chat.id}")
