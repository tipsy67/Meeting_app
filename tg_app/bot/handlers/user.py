import os

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery

from tg_app.bot.databases.sql_requests import set_user
from tg_app.bot.keyboards import userkb

user = Router ()

@user.message(CommandStart())
async def start(message: Message):
    await set_user(message.from_user.id)
    await message.answer('Links bellow', reply_markup=userkb.main)

@user.callback_query(F.data=='donate')
async def top_up(callback_query: CallbackQuery):
        await callback_query.bot.send_invoice(
        callback_query.from_user.id,
        title="Подписка на бота",
        description="Активация подписки на бота на 1 месяц",
        provider_token=(os.getenv('TG_PAYMASTER')),
        currency="rub",
        photo_url="https://cs15.pikabu.ru/post_img/big/2024/08/24/10/1724515420160483017.png",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=[
            LabeledPrice(label='Подписка на бота (1 месяц)', amount=30000)
        ],
        start_parameter="",
        payload="test-invoice-payload")

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

@user.pre_checkout_query() # Регистрирует функцию для обработки события
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@user.message(F.successful_payment)
async def successful_payment(message: Message):
    payment_info = message.successful_payment
    await message.answer(
        f"Спасибо за оплату, {message.from_user.first_name}! 🎉\n"
        f"Вы успешно активировали подписку на 1 месяц.\n\n"
        f"Детали платежа: {payment_info.total_amount / 100} {payment_info.currency}\n"
        f"Если у вас возникнут вопросы, напишите в поддержку."
    )
