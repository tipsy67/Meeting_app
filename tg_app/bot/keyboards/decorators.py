from functools import wraps
from typing import Callable, Awaitable

from aiogram.types import CallbackQuery


def delete_previous_message(handler: Callable[[CallbackQuery], Awaitable[None]]):
    """
    Декоратор для автоматического удаления предыдущего сообщения
    перед выполнением обработчика CallbackQuery
    """

    @wraps(handler)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        try:
            await callback.message.delete()
        except Exception as e:
            await callback.answer(f"Ошибка удаления: {e}", show_alert=True)
            raise
        finally:
            await callback.answer()

        return await handler(callback, *args, **kwargs)

    return wrapper