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
            func = await handler(callback, *args, **kwargs)
        except Exception as e:
            await callback.answer(f"Ошибка удаления: {e}", show_alert=True)
            raise
        finally:
            await callback.answer()

        return func

    return wrapper

async def handle_api_response(response, callback: CallbackQuery, l10n=None):
    """
    Обработчик ошибок
    :param response: ответ АПИ
    :param callback:
    :param l10n: локализация
    :return:
    """
    if response.get('error'):
        error_msg = f"{response['error']}: {response.get('detail', '')}"
        await callback.message.answer(error_msg)
        await callback.answer()
        return False
    return True