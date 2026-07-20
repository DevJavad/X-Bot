from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder as Builder


from app.bot.routers.core import BackAction, BackCB

from .data import AdminAction as Action, AdminCB as CB


def management_button() -> Markup:
    builder = Builder()

    builder.button(
        text=_("button:management:products"),
        style=ButtonStyle.PRIMARY,
        callback_data=CB(action=Action.PRODUCTS),
    )

    builder.button(
        text=_("button:back"),
        style=ButtonStyle.DANGER,
        callback_data=BackCB(action=BackAction.MAIN),
    )
    builder.adjust(1, 1)
    return builder.as_markup()