
from aiogram import Bot
from api_app.core.config import settings

async def bot_send_message(user_id: int, text: str):
    async with Bot(token=settings.tg.token) as bot:
        await bot.send_message(user_id, text)
        print(f"Сообщение отправлено пользователю {user_id}") #todo: add logging

