import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _

from app.database.models import User
from app.settings import Config
from app.utils.functions import is_member

from .buttons import start_button
from .data import CoreAction as Action, CoreCB as CB, BackCB, BackAction

router = Router(name=__name__)
logger = logging.getLogger(__name__)


def start_data(message: Message, user: User) -> tuple:
    return _("message:start").format(name=message.from_user.full_name), start_button(user.role)


@router.message(CommandStart())
async def start(message: Message, user: User, state: FSMContext) -> None:
    await state.clear()

    text, markup = start_data(message, user)
    return await message.answer(text, reply_markup=markup)


@router.callback_query(F.data == Action.JOINED)
async def joined(query: CallbackQuery, user: User, config: Config):
    if not await is_member(query.message.bot, config, user.user_id):
        return await query.answer(_("notification:join_required"), True)

    text, markup = start_data(query.message, user)
    return await query.message.edit_text(text, reply_markup=markup)


@router.callback_query(BackCB.filter(F.action == BackAction.MAIN))
async def back(query: CallbackQuery, user: User, state: FSMContext) -> None:
    await state.clear()

    text, markup = start_data(query.message, user)
    return await query.message.edit_text(text, reply_markup=markup)