from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def create_buttons(l10n, buttons_data: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    """
    Формирование клавиатуры из списка кортежей с описанием кнопок,
    вида (заголовок, коллбэк_дата)
    :param l10n: локализация
    :param buttons_data: список с описанием кнопок
    :return:
    """
    keyboard_buttons: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=l10n.format_value(text_key) if l10n is not None else text_key,
                callback_data=callback_key,
            )
        ]
        for text_key, callback_key in buttons_data
    ]
    # print(keyboard_buttons)
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def get_web_app():
    timestamp = int(datetime.now().timestamp())
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть WebApp",
                    web_app=WebAppInfo(
                        url=f"https://2deyhh-37-44-40-134.ru.tuna.am/index.html?force_reload={timestamp}"
                    ),
                )
            ]
        ]
    )
    return keyboard


def get_unblock_keyboard(l10n) -> InlineKeyboardMarkup:
    buttons_data = [
        ("kb_unblock", "kb_unblock"),
    ]

    return create_buttons(l10n, buttons_data)
