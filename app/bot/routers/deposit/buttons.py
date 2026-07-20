from aiogram.enums import ButtonStyle
from aiogram.types import CopyTextButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.settings import Config

from .data import DepositAction as Action, DepositCB as CB


def deposit_button(config: Config) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=_("button:copy"),
        # icon_custom_emoji_id=Emoji.CARD,
        style=ButtonStyle.PRIMARY,
        copy_text=CopyTextButton(text=config.payment.card_number),
    )

    builder.button(
        text=_("button:cancel"),
        # icon_custom_emoji_id=Emoji.CANCEL,
        style=ButtonStyle.DANGER,
        callback_data=CB(action=Action.CANCEL),
    )

    builder.adjust(1, 1)
    return builder.as_markup()


def confirm_button(invoice_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=_("button:deposit:confirm"),
        # icon_custom_emoji_id=Emoji.CONFIRM,
        style=ButtonStyle.SUCCESS,
        callback_data=CB(action=Action.CONFIRM, invoice_id=invoice_id)
    )

    builder.button(
        text=_("button:deposit:reject"),
        # icon_custom_emoji_id=Emoji.REJECT,
        style=ButtonStyle.DANGER,
        callback_data=CB(action=Action.REJECT, invoice_id=invoice_id),
    )

    return builder.as_markup()