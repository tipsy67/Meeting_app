import os

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery

from tg_app.bot.databases.mongo_requests import set_user
from tg_app.bot.keyboards import userkb
# from aiogram.utils.i18n import gettext as _


user = Router ()

class Choice(StatesGroup):
    select_amount = State()

@user.message(CommandStart())
async def start(message: Message, l10n):
    await set_user(message.from_user)
    print(message.from_user)
    await message.answer(l10n.format_value('welcome'), reply_markup=userkb.main)

@user.callback_query(F.data=='donate')
async def top_up(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.reply(
        text="Введите сумму, которую вы хотите пополнить:",
        reply_to_message_id=callback_query.message.message_id
    )
    await callback_query.answer()
    await state.set_state(Choice.select_amount)


@user.message(Choice.select_amount)
async def donation_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount < 10:
            await message.answer("Минимальная сумма пополнения — 10 рублей. Попробуйте снова.")
            return
        amount_in_cents = amount * 100

        await message.bot.send_invoice(
            chat_id=message.from_user.id,
            title="Пополнение",
            description=f"Ваше пополнение на сумму {amount} руб.",
            provider_token=os.getenv('TG_PAYMASTER'),
            currency="rub",
            prices=[LabeledPrice(label="Пополнение", amount=amount_in_cents)],
            payload="donation"
        )
        await state.clear()

    except ValueError:
        await message.answer("Введите корректное число (целое число больше 10).")

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
