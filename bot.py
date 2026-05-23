import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TELEGRAM_BOT_TOKEN
from handlers import start, dashboard, upload, settings

async def main():
    if not TELEGRAM_BOT_TOKEN:
        logging.error("No TELEGRAM_BOT_TOKEN provided in environment variables.")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(dashboard.router)
    dp.include_router(settings.router)
    dp.include_router(upload.router)

    logging.info("Starting bot with Dynamic Engine settings...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
