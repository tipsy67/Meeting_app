from logging.config import listen

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard(l10n) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value('kb_main_speaker'),
                    callback_data='kb_main_speaker'
                )
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value('kb_main_listener'),
                    callback_data='kb_main_listener'
                )
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value('kb_main_help'),
                    callback_data='kb_main_help'
                )
            ],
        ]
    )

def get_unblock_keyboard(l10n) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value('kb_unblock'),
                    callback_data='kb_unblock'
                )
            ],
        ]
    )

def get_speaker_keyboard(l10n) -> InlineKeyboardMarkup:
    pass

def get_listener_keyboard(l10n) -> InlineKeyboardMarkup:
    pass