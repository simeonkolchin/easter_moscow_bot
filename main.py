import asyncio
import aioschedule
from config_reader import config
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import main_page, admin_page
import sqlite_db
from utils import send_subscription_reminder


async def on_startup():
    await sqlite_db.db_connect()
    print('Successful db connect ✅')


async def scheduler():
    """Асинхронный цикл для выполнения запланированных задач."""
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def notification(bot):
    aioschedule.every().day.at("02:42").do(send_subscription_reminder, bot=bot)
    asyncio.create_task(scheduler())


async def main():
    await on_startup()
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(main_page.router, admin_page.router)
    await bot.delete_webhook(drop_pending_updates=True)
    # await notification(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
