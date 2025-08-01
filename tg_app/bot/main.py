import asyncio
import os

from aiogram import Bot, Dispatcher, F, types
from dotenv import load_dotenv

from tg_app.bot.middlewares.language import FluentL10nMiddleware

load_dotenv()

from handlers.user import user


async def main():
    bot = Bot(token=os.environ.get("TG_TOKEN"))
    dp = Dispatcher()
    dp.update.middleware(FluentL10nMiddleware("locales"))
    dp.include_routers(
        user,
    )
    dp.startup.register(startup)
    await dp.start_polling(bot)


async def startup():
    pass


if __name__ == "__main__":
    print("Bot starting...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot canceled.")
