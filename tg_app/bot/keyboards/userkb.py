from logging.config import listen
from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


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


def get_users_button_list(
    users: list[dict], name: str, included_users: Optional[set[int]] = None
) -> list[tuple[str, str]]:
    """
    Формирование описания кнопок со списком пользователей
    :param users: все пользователи
    :param name: параметр для разделения коллбэк_дата на группы
    :param included_users: включенные в группу
    :return:
    """

    buttons_data = [
        (
            (
                f'{'' if included_users is None or user.get('_id') not in included_users else '✅ '}'
                f'{user.get('username')}({user.get('full_name')})'
            ),
            f'add:{name}:{str(user.get('_id'))}',
        )
        for user in users
    ]

    return buttons_data


def get_main_keyboard(l10n) -> InlineKeyboardMarkup:
    buttons_data = [
        ('kb_main_speaker', 'kb_main_speaker'),
        ('kb_main_listener', 'kb_main_listener'),
        ('kb_main_subscribe', 'kb_main_subscribe'),
        ('kb_main_help', 'kb_main_help'),
    ]

    return create_buttons(l10n, buttons_data)


def get_unblock_keyboard(l10n) -> InlineKeyboardMarkup:
    buttons_data = [
        ('kb_unblock', 'kb_unblock'),
    ]

    return create_buttons(l10n, buttons_data)


def get_speaker_keyboard(l10n) -> InlineKeyboardMarkup:
    buttons_data = [
        ('kb_new_lecture', 'kb_new_lecture'),
        ('kb_open_lecture', 'kb_open_lecture'),
        ('kb_main_menu', 'kb_main_menu'),
    ]

    return create_buttons(l10n, buttons_data)


def get_users_list(
    l10n, users: list[dict], name: str, included_users: Optional[set[int]] = None
) -> InlineKeyboardMarkup:

    kb1 = create_buttons(None, get_users_button_list(users, name, included_users))
    additional_buttons = [('kb_main_menu', 'kb_main_menu')]
    if name == 'listener':
        additional_buttons[:0] = [('kb_save_lecture', 'kb_save_lecture')]

    kb2 = create_buttons(l10n, additional_buttons)
    merged_kb = InlineKeyboardMarkup(
        inline_keyboard=[*kb1.inline_keyboard, *kb2.inline_keyboard]
    )
    return merged_kb


async def get_lectures_list(l10n, lectures: list[dict]) -> InlineKeyboardMarkup:
    buttons_data = [
        (
            lecture.get('name'),
            f'open:lecture:{str(lecture.get('_id'))}:{lecture.get('name')}',
        )
        for lecture in lectures
    ]
    kb1 = create_buttons(None, buttons_data)
    additional_buttons = [('kb_back', 'kb_main_speaker')]
    kb2 = create_buttons(l10n, additional_buttons)
    merged_kb = InlineKeyboardMarkup(
        inline_keyboard=[*kb1.inline_keyboard, *kb2.inline_keyboard]
    )
    return merged_kb


def get_lecture_keyboard(l10n) -> InlineKeyboardMarkup:
    buttons_data = [
        ('kb_new_meeting', 'kb_new_meeting'),
        ('kb_edit_lecture', 'kb_edit_lecture'),
        ('kb_back', 'kb_open_lecture'),
        ('kb_main_menu', 'kb_main_menu'),
    ]

    return create_buttons(l10n, buttons_data)


def get_lecture_users_list(
    l10n,
    users: list[dict],
    name: str,
    included_users: Optional[set[int]] = None,
    lecture: str = None,
) -> InlineKeyboardMarkup:

    kb1 = create_buttons(None, get_users_button_list(users, name, included_users))
    additional_buttons = [
        ('kb_delete_lecture', f'delete:lecture:{lecture}'),
        ('kb_back', f'open:lecture:{lecture}'),
    ]

    kb2 = create_buttons(l10n, additional_buttons)
    merged_kb = InlineKeyboardMarkup(
        inline_keyboard=[*kb1.inline_keyboard, *kb2.inline_keyboard]
    )
    return merged_kb

def get_web_app():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Открыть WebApp",
                web_app=WebAppInfo(url="https://0i6p1a-37-44-40-134.ru.tuna.am/index.html")
            )]
        ]
    )
    return keyboard
