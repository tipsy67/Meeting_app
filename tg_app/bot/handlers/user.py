import os


from aiogram import Router
from aiogram.filters import CommandStart

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from tg_app.bot.databases import api_requests
from tg_app.bot.keyboards import userkb


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

    # await message.answer(
    #     l10n.format_value('welcome'), reply_markup=userkb.get_main_keyboard(l10n)
    # )
    await message.answer( l10n.format_value('welcome'),
                           reply_markup=userkb.get_web_app())

