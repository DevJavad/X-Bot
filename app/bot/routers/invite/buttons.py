from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder as Builder

from app.bot.routers.core import BackCB, BackAction


def invite_button(invite_link: str) -> Markup:
    builder = Builder()

    builder.button(
        text=_("button:sheare_invite_link"),
        style=ButtonStyle.PRIMARY,
        url=f"https://t.me/share/url?url={invite_link}",
    )

    builder.button(
        text=_("button:back"),
        style=ButtonStyle.DANGER,
        callback_data=BackCB(action=BackAction.MAIN),
    )

    builder.adjust(1, 1)
    return builder.as_markup()