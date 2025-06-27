from logging.config import listen
from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_buttons(l10n, buttons_data: list[tuple[str, str]]) -> InlineKeyboardMarkup:

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

    buttons_data = [
        (
            (f'{'' if included_users is None or user.get('_id') not in included_users else '✅ '}'
             f'{user.get('username')}({user.get('full_name')})'),

            f'add:{name}:{str(user.get('_id'))}',
        )
        for user in users
    ]

    kb1 = create_buttons(None, buttons_data)
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
        (lecture.get('name'),
        f'edit:lecture:{str(lecture.get('_id'))}:{lecture.get('name')}') for lecture in lectures
    ]
    kb1 = create_buttons(None, buttons_data)
    additional_buttons = [('kb_back', 'kb_main_speaker')]
    kb2 = create_buttons(l10n, additional_buttons)
    merged_kb = InlineKeyboardMarkup(
        inline_keyboard=[*kb1.inline_keyboard, *kb2.inline_keyboard]
    )
    return merged_kb
