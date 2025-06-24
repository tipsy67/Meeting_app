import os
from typing import Annotated

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from tg_app.bot.databases.api_requests import add_speaker, get_speakers, set_user, get_listeners
from tg_app.bot.keyboards import userkb
from tg_app.bot.keyboards.decorators import delete_previous_message

user = Router()


class Choice(StatesGroup):
    select_amount = State()


# START
@user.message(CommandStart())
async def start(message: Message, l10n):
    response = await set_user(message.from_user)

    err = response.get('error')
    if err is not None:
        await message.answer(f'{err}: {response.get('detail')}')
        return

    text = response.get('is_blocked')
    if text:
        await message.answer(
            l10n.format_value('blocked') + f'\n{text}',
            reply_markup=userkb.get_unblock_keyboard(l10n),
        )
        return

    await message.answer(
        l10n.format_value('welcome'), reply_markup=userkb.get_main_keyboard(l10n)
    )


# MAIN MENU
@user.callback_query(F.data == 'kb_main_menu')
@delete_previous_message
async def main_menu(callback: CallbackQuery, l10n):
    await callback.message.answer(
        l10n.format_value('kb_main_menu'), reply_markup=userkb.get_main_keyboard(l10n)
    )

# SPEAKER MENU
@user.callback_query(F.data == 'kb_main_speaker')
@delete_previous_message
async def choose_speaker(callback: CallbackQuery, l10n):
    await callback.message.answer(
        l10n.format_value('kb_main_speaker'),
        reply_markup=userkb.get_speaker_keyboard(l10n),
    )
    await callback.answer()


@user.callback_query(F.data == 'kb_new_lecture')
@delete_previous_message
async def choose_speaker(callback: CallbackQuery, l10n, temp_data:dict):
    response = await get_listeners(callback.from_user.id)
    err = response.get('error')
    if err is not None:
        await callback.message.answer(f'{err}: {response.get('detail')}')
        await callback.answer()
        return

    temp_data[str(callback.from_user.id)] = set()

    await callback.message.answer(
        l10n.format_value('listeners'),
        reply_markup=userkb.get_users_list(l10n, response['listeners'], 'listener'),
    )
    await callback.answer()

@user.callback_query(F.data.startswith('add:listener:'))
@delete_previous_message
async def choose_speaker(callback: CallbackQuery, l10n, temp_data:dict):
    _, _, listener_id = callback.data.split(':')
    listener_id = int(listener_id)
    set_listeners = temp_data[str(callback.from_user.id)]
    if listener_id in set_listeners:
        set_listeners.remove(listener_id)
    else:
        set_listeners.add(listener_id)

    response = await get_listeners(callback.from_user.id)
    err = response.get('error')
    if err is not None:
        await callback.message.answer(f'{err}: {response.get('detail')}')
        await callback.answer()
        return

    await callback.message.answer(
        l10n.format_value('listeners'),
        reply_markup=userkb.get_users_list(l10n, response['listeners'], 'listener', set_listeners),
    )
    await callback.answer()

# LISTENER MENU
@user.callback_query(F.data == 'kb_main_listener')
@delete_previous_message
async def choose_speaker(callback: CallbackQuery, l10n):
    response = await get_speakers()
    await callback.message.answer(
        l10n.format_value('speakers'),
        reply_markup=userkb.get_users_list(l10n, response, 'speaker'),
    )
    await callback.answer()


@user.callback_query(F.data.startswith('add:speaker:'))
@delete_previous_message
async def choose_speaker(callback: CallbackQuery, l10n):
    _, _, speaker_id = callback.data.split(':')
    response = await add_speaker(int(speaker_id), callback.from_user.id)
    err = response.get('error')
    if err is not None:
        await callback.message.answer(f'{err}: {response.get('detail')}')
        await callback.answer()
        return
    # await callback.message.answer()
    await callback.message.answer(l10n.format_value('add_to_speaker'), reply_markup=userkb.get_main_keyboard(l10n))
    await callback.answer()


@user.callback_query(F.data == 'donate')
async def top_up(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.reply(
        text="Введите сумму, которую вы хотите пополнить:",
        reply_to_message_id=callback_query.message.message_id,
    )
    await callback_query.answer()
    await state.set_state(Choice.select_amount)


@user.message(Choice.select_amount)
async def donation_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount < 10:
            await message.answer(
                "Минимальная сумма пополнения — 10 рублей. Попробуйте снова."
            )
            return
        amount_in_cents = amount * 100

        await message.bot.send_invoice(
            chat_id=message.from_user.id,
            title="Пополнение",
            description=f"Ваше пополнение на сумму {amount} руб.",
            provider_token=os.getenv('TG_PAYMASTER'),
            currency="rub",
            prices=[LabeledPrice(label="Пополнение", amount=amount_in_cents)],
            payload="donation",
        )
        await state.clear()

    except ValueError:
        await message.answer("Введите корректное число (целое число больше 10).")


@user.callback_query(F.data == 'menu')
async def menu(callback_query: CallbackQuery):
    await callback_query.answer('Our menu', show_alert=True)
    await callback_query.message.answer('Menu not available')


@user.callback_query(F.data == 'profile')
async def profile(callback_query: CallbackQuery):
    await callback_query.message.answer('Profile not available')


@user.callback_query(F.data == 'order')
async def order(callback_query: CallbackQuery):
    await callback_query.message.answer('Order not available')


@user.pre_checkout_query()  # Регистрирует функцию для обработки события
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
