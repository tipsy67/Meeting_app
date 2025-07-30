"""
Module for Telegram API staff
"""

import httpx
from aiogram import Bot

from live_kit_app.config import API_API_URL, TG_TOKEN


async def send_message_to_listeners(conference_id: str, message: str, name: str):
    """
    Send message to conference`s listeners
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_API_URL}/conferences/{conference_id}")
            if response.status_code == 200:
                data = response.json()
                listeners = [user.get("user_id") for user in data.get("listeners")]
                if listeners:
                    async with Bot(token=TG_TOKEN) as bot:
                        message_to_tg = (
                            "<b>Сообщение из чата конференции:</b>\n"
                            f"<i>автор: {name}\n\n</i>"
                            f"Сообщение:\n<blockquote>{message}</blockquote>"
                        )
                        for listener in listeners:
                            await bot.send_message(
                                listener, text=message_to_tg, parse_mode="HTML"
                            )
        except Exception as e:
            print(f"Error: {e}")
