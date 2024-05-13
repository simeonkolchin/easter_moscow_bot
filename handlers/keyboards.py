from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
import sqlite_db
import datetime
import random
from files import questions as q


def get_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Добавить в календарь🗓️", callback_data="add_calendar"),
                types.InlineKeyboardButton(text="Задать вопрос✝️", callback_data="ask_a_question"),
                types.InlineKeyboardButton(text="Больше о мероприятии⛪", url='https://пасхамосква.рф/'),
                types.InlineKeyboardButton(text="О создателях бота⚙️", callback_data="information_create"),
                types.InlineKeyboardButton(text="Получить подарок🎁", callback_data="get_gift"),
                width=1)
    return builder


def video():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=f"Что такое пасха?", web_app=WebAppInfo(url='https://Easter-rbc.ru/gospel')),
        width=1)
    return builder


def whathappenthere():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Как выглядит это событие🤩", callback_data="w"), width=1)
    return builder


def text_4():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Открыть сайт", url='https://Easter-rbc.ru/gospel'), width=1)
    return builder


def text_5():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Добавить в календарь", url='https://tools.emailmatrix.ru/event-generator/?format=ics&id=404076'), width=1)
    return builder


def calendar():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Добавить в календарь", url='https://tools.emailmatrix.ru/event-generator/?format=ics&id=404076'), width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder


def information_easter_1():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Как Пасха связана с Иисусом?", callback_data="information_easter_2"),
                width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder


def information_easter_2():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"И каков же смысл?", callback_data="information_easter_3"),
                width=1)
    return builder

def information_easter_3():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Главное меню »", callback_data="start"),
                width=1)
    return builder

def information_event():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="пасхамосква.рф", url='https://пасхамосква.рф/'),
                width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder

def information_create():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder

def get_gift():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder

def questions():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="ask_a_question"),
                width=1)
    return builder


def help_callback():
    builder = InlineKeyboardBuilder()
    m = []
    for i in range(0, len(q.questions)):
        m.append(types.InlineKeyboardButton(text=f"{q.questions[i]}", callback_data=f"question_{i}"))
    builder.row(*m, width=1)
    builder.row(types.InlineKeyboardButton(text=f"В чем заключается суть христианства?", web_app=WebAppInfo(url='https://easter-rbc.ru/gospel')), width=1)
    builder.row(types.InlineKeyboardButton(text=f"Задать свой вопрос", callback_data="cin_question"), width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder

def cin_question():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="ask_a_question"),
                width=1)
    return builder


def help_router():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Главное меню »", callback_data="start"),
                width=1)
    return builder


def reply_help(id):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Ответить", callback_data=f"reply_help_{id}"),
                width=1)
    return builder


def send_invoice_edit_text():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Добавить фото", callback_data=f"send_invoice_add_photo"),
                types.InlineKeyboardButton(text="Изменить текст", callback_data=f"send_invoice_edit_text"),
                types.InlineKeyboardButton(text="Отправить", callback_data=f"send_invoice_send_message"),
                width=1)
    return builder

def send_invoice_edit_photo():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Изменить фото", callback_data=f"send_invoice_add_photo"),
                types.InlineKeyboardButton(text="Изменить текст", callback_data=f"send_invoice_edit_text"),
                types.InlineKeyboardButton(text="Отправить", callback_data=f"send_invoice_send_message"),
                width=1)
    return builder