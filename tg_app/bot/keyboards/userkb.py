from logging.config import listen

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


def get_users_list(l10n, users: list[str]) -> InlineKeyboardMarkup:
    buttons_data = [
        (
            f'{user.get('username')}({user.get('full_name')})',
            f'add:speaker:{str(user.get('_id'))}',
        )
        for user in users
    ]

    kb1 = create_buttons(None, buttons_data)
    kb2 = create_buttons(l10n,  [('kb_main_menu', 'kb_main_menu')])
    merged_kb = InlineKeyboardMarkup(inline_keyboard=[
        *kb1.inline_keyboard,
        *kb2.inline_keyboard
    ])
    return merged_kb

