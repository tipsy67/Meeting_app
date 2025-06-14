from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Menu', callback_data='menu')],
    [InlineKeyboardButton(text='Order', callback_data='order')],
    [InlineKeyboardButton(text='Profile', callback_data='profile')],
    [InlineKeyboardButton(text='Donate', callback_data='donate')],
])