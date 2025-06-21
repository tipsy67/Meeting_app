from logging.config import listen

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_buttons(l10n, buttons_data: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    keyboard_buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text=l10n.format_value(text_key),
            callback_data=callback_key
        )] for text_key, callback_key in buttons_data
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

def get_main_keyboard(l10n) -> InlineKeyboardMarkup:
    buttons_data = [
        ('kb_main_speaker', 'kb_main_speaker'),
        ('kb_main_listener', 'kb_main_listener'),
        ('kb_main_subscribe', 'kb_main_subscribe'),
        ('kb_main_help', 'kb_main_help')
    ]

    return create_buttons(l10n, buttons_data)


def get_unblock_keyboard(l10n) -> InlineKeyboardMarkup:
    buttons_data = [
        ('kb_unblock', 'kb_unblock'),
    ]

    return create_buttons(l10n, buttons_data)



def get_speaker_keyboard(l10n) -> InlineKeyboardMarkup:
    pass


def get_listener_keyboard(l10n, speakers: list[str]) -> InlineKeyboardMarkup:
    buttons_data = [ (user, user) for user in speakers]

    return create_buttons(l10n, buttons_data)