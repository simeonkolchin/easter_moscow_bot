import sqlite_db
import datetime


async def send_subscription_reminder(bot):
    now = datetime.datetime.now()
    if now.date() == datetime.date(year=2024, day=21, month=4):
        users = await sqlite_db.get_users()
        all = [i[2] for i in users]
        for i in all:
            await bot.send_message(chat_id=1647407069, text="Напоминание о событии")
