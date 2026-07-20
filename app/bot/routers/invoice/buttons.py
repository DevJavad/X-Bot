from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.routers.core import BackAction, BackCB
from app.database.models import Invoice

from .data import InvoiceAction as Acrion, InvoiceCB as CB


def invoices_button(
    invoices: list[Invoice],
    page: int = 0,
    pages: int = 1,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for invoice in invoices:
        builder.button(
            text=f"{invoice.invoice_id} | {int(invoice.amount):,}",
            style=ButtonStyle.PRIMARY,
            callback_data=CB(
                action=Acrion.DETAIL, invoice_id=invoice.invoice_id
            ),
        )
    builder.adjust(1)

    nav_builder = InlineKeyboardBuilder()

    if page > 0:
        nav_builder.button(
            text=_("button:previous"),
            # icon_custom_emoji_id=Emoji.PREVIOUS,
            style=ButtonStyle.SUCCESS,
            callback_data=CB(action=Acrion.PAGE, page=page - 1),
        )

    if page < pages - 1:
        nav_builder.button(
            text=_("button:next"),
            # icon_custom_emoji_id=Emoji.NEXT,
            style=ButtonStyle.SUCCESS,
            callback_data=CB(action=Acrion.PAGE, page=page + 1),
        )

    if nav_builder.buttons:
        nav_builder.adjust(2)
        builder.attach(nav_builder)

    builder.row(
        InlineKeyboardButton(
            text=_("button:back"),
            # icon_custom_emoji_id=Emoji.BACK,
            style=ButtonStyle.DANGER,
            callback_data=BackCB(action=BackAction.MAIN).pack(),
        )
    )

    return builder.as_markup()


def invoice_detail_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=_("button:back"),
        # icon_custom_emoji_id=Emoji.BACK,
        style=ButtonStyle.DANGER,
        callback_data=CB(action=Acrion.BACK),
    )

    return builder.as_markup()
