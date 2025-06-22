import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from dotenv import load_dotenv

from tg_app.bot.databases.sql_models import async_main
from tg_app.bot.middlewares.language import FluentL10nMiddleware

load_dotenv()

from handlers.user import user

async def main():
    bot = Bot(token=os.environ.get("TG_TOKEN"))
    dp = Dispatcher()
    dp.update.middleware(FluentL10nMiddleware('locales'))
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

