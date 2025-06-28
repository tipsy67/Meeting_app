import os
from typing import Annotated

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from tg_app.bot.databases import api_requests
from tg_app.bot.keyboards import userkb
from tg_app.bot.keyboards.service import delete_previous_message, handle_api_response

user = Router()

class LectureName(StatesGroup):
    waiting_for_object_name = State()

class Choice(StatesGroup):
    select_amount = State()


# START
@user.message(CommandStart())
async def start(message: Message, l10n):
    response = await api_requests.set_user(message.from_user)

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
async def cb_main_menu(callback: CallbackQuery, l10n):
    await callback.message.answer(
        l10n.format_value('kb_main_menu'), reply_markup=userkb.get_main_keyboard(l10n)
    )


## SPEAKER MENU
@user.callback_query(F.data == 'kb_main_speaker')
@delete_previous_message
async def cb_speaker_menu(callback: CallbackQuery, l10n):
    await callback.message.answer(
        l10n.format_value('kb_main_speaker'),
        reply_markup=userkb.get_speaker_keyboard(l10n),
    )

#### New lecture
@user.callback_query(F.data == 'kb_new_lecture')
@delete_previous_message
async def cb_get_listeners(callback: CallbackQuery, l10n, state: FSMContext):
    response = await api_requests.get_listeners(callback.from_user.id)
    if not await handle_api_response(response, callback, l10n):
        return

    await state.update_data(listeners=list())

    await callback.message.answer(
        l10n.format_value('listeners'),
        reply_markup=userkb.get_users_list(l10n, response['listeners'], 'listener'),
    )

###### Listener list
@user.callback_query(F.data.startswith('add:listener:'))
@delete_previous_message
async def cb_add_listener(callback: CallbackQuery, l10n, state: FSMContext):
    *_, listener_id = callback.data.split(':')
    listener_id = int(listener_id)

    listeners = await state.get_data()
    set_listeners = set(listeners.get('listeners'))
    if listener_id in set_listeners:
        set_listeners.remove(listener_id)
    else:
        set_listeners.add(listener_id)
    await state.update_data(listeners=set_listeners)

    response = await api_requests.get_listeners(callback.from_user.id)
    if not await handle_api_response(response, callback, l10n):
        return

    await callback.message.answer(
        l10n.format_value('listeners'),
        reply_markup=userkb.get_users_list(
            l10n, response['listeners'], 'listener', set_listeners
        ),
    )

###### Save lecture
@user.callback_query(F.data == 'kb_save_lecture')
@delete_previous_message
async def cb_get_lecture_name(callback: CallbackQuery, l10n, state: FSMContext):
    bot_msg = await callback.message.answer(l10n.format_value('get_name_lecture'))
    await state.update_data(bot_msg_id=bot_msg.message_id)
    await state.set_state(LectureName.waiting_for_object_name)

###### Enter name of lecture
@user.message(LectureName.waiting_for_object_name)
async def cb_save_lecture(message: Message, l10n, state: FSMContext, bot: Bot):
    data = await state.get_data()
    bot_msg_id = data['bot_msg_id']
    await bot.delete_message(message.chat.id, bot_msg_id)

    await message.delete()
    name_lecture = message.text.strip()
    if len(name_lecture) < 3:
        bot_msg = await message.answer(l10n.format_value('wrong_name_lecture'))
        await state.update_data(bot_msg_id=bot_msg.message_id)
        return

    listeners = await state.get_data()
    set_listeners = set(listeners.get('listeners'))
    cleaned_text = " ".join(name_lecture.split())
    name_lecture = cleaned_text.replace(" ", ".")
    name_lecture = f"{message.from_user.id}_{name_lecture}"

    response = await api_requests.save_lecture(name_lecture, set_listeners)

    await message.answer(
        l10n.format_value('save_lecture_done'),
        reply_markup=userkb.get_speaker_keyboard(l10n),
    )
    # await state.clear()
    await state.set_state(None)

#### Open lecture
@user.callback_query(F.data == 'kb_open_lecture')
@delete_previous_message
async def cb_open_lecture(callback: CallbackQuery, l10n):
    response = await api_requests.get_all_lectures(callback.from_user.id)
    if not await handle_api_response(response, callback, l10n):
        return

    await callback.message.answer(
        l10n.format_value('open_lecture'),
        reply_markup=await userkb.get_lectures_list(l10n, response['lectures']),
    )

####
#### Edit lecture
@user.callback_query(F.data.startswith('open:lecture:'))
@delete_previous_message
async def cb_open_lecture(callback: CallbackQuery, l10n, state: FSMContext):
    *_, lecture = callback.data.split(':')

    response = await api_requests.get_listeners_from_lecture(callback.from_user.id, lecture)
    if not await handle_api_response(response, callback, l10n):
        return

    set_listeners = set([listener.get('_id') for listener in response['listeners']])
    await state.update_data(listeners=list(set_listeners))
    await state.update_data(lecture=lecture)

    await callback.message.answer(
        f'{l10n.format_value('kb_lecture')} {lecture}',
        reply_markup=userkb.get_lecture_keyboard(l10n),
    )

###### Creating new meet
@user.callback_query(F.data == 'kb_new_meeting')
async def cb_new_meeting(callback: CallbackQuery, l10n, state: FSMContext):
    await callback.message.answer('Creating new meeting...')

###### Edit users in lecture
@user.callback_query(F.data == 'kb_edit_lecture')
@delete_previous_message
async def cb_get_listeners_from_lecture(callback: CallbackQuery, l10n, state: FSMContext):

    data = await state.get_data()
    set_listeners = set(data.get('listeners'))
    lecture = data.get('lecture')

    response = await api_requests.get_listeners(callback.from_user.id)
    if not await handle_api_response(response, callback, l10n):
        return

    await callback.message.answer(
        f'{l10n.format_value('kb_lecture')} {lecture}',
        reply_markup=userkb.get_lecture_users_list(
            l10n, response['listeners'], 'listener', set_listeners, lecture
        ),
    )

# LISTENER MENU
@user.callback_query(F.data == 'kb_main_listener')
@delete_previous_message
async def cb_get_speakers(callback: CallbackQuery, l10n):
    response = await api_requests.get_speakers()
    if not await handle_api_response(response, callback, l10n):
        return

    await callback.message.answer(
        l10n.format_value('speakers'),
        reply_markup=userkb.get_users_list(l10n, response['speakers'], 'speaker'),
    )

## Add user to speaker
@user.callback_query(F.data.startswith('add:speaker:'))
@delete_previous_message
async def cb_add_speaker(callback: CallbackQuery, l10n):
    *_, speaker_id = callback.data.split(':')
    response = await api_requests.add_speaker(int(speaker_id), callback.from_user.id)
    if not await handle_api_response(response, callback, l10n):
        return

    await callback.message.answer(
        l10n.format_value('add_to_speaker'), reply_markup=userkb.get_main_keyboard(l10n)
    )

#END MENU


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
