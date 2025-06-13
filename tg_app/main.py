import asyncio
import os
import re

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

from bot.handlers.user import user

async def main():
    bot = Bot(token=os.environ.get("TG_TOKEN"))
    dp = Dispatcher()
    dp.include_routers(user,)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('Bot starting...')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot canceled.')

