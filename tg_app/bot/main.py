import asyncio
import os
import re
from pathlib import Path

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv

from tg_app.bot.databases.sql_models import async_main
from tg_app.bot.middlewares.language import lang_middleware

load_dotenv()

from handlers.user import user

async def main():
    bot = Bot(token=os.environ.get("TG_TOKEN"))
    dp = Dispatcher()
    dp.message.middleware(lang_middleware)
    dp.include_routers(user,)
    dp.startup.register(startup)
    await dp.start_polling(bot)

async def startup():
    await async_main()

if __name__ == '__main__':
    print('Bot starting...')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot canceled.')

