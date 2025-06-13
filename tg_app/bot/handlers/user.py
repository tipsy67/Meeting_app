from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from tg_app.bot.keyboards import userkb

user = Router ()

@user.message(CommandStart())
async def start(message: Message):
    await message.answer('Links bellow', reply_markup=userkb.main)

@user.callback_query(F.data=='menu')
async def menu (callback_query: CallbackQuery):
    await callback_query.answer('Our menu',show_alert=True)
    await callback_query.message.answer('Menu not available')

@user.callback_query(F.data=='profile')
async def profile (callback_query: CallbackQuery):
    await callback_query.message.answer('Profile not available')

@user.callback_query(F.data=='order')
async def order (callback_query: CallbackQuery):
    await callback_query.message.answer('Order not available')
