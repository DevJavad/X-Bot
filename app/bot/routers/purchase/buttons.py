from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


from app.bot.routers.core import BackAction, BackCB, CoreAction, CoreCB
from app.database.models import Product

from .data import PurchaseAction as Action, PurchaseCB as CB


def purchase_button(products: list[Product]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for product in products:
        builder.button(
            text=f"{product.name} - {int(product.price):,}",
            style=ButtonStyle.PRIMARY,
            callback_data=CB(action=Action.DETAIL, product_id=product.id),
        )
    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(
            text=_("button:back"),
            # icon_custom_emoji_id=Emoji.BACK,
            style=ButtonStyle.DANGER,
            callback_data=BackCB(action=BackAction.MAIN).pack(),
        )
    )
    return builder.as_markup()


def product_detail_button(product: Product) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=_("button:purchase"),
        # icon_custom_emoji_id=Emoji.PURCHASE,
        style=ButtonStyle.PRIMARY,
        callback_data=CB(action=Action.BUY, product_id=product.id),
    )

    builder.button(
        text=_("button:deposit"),
        # icon_custom_emoji_id=Emoji.DEPOSIT,
        style=ButtonStyle.PRIMARY,
        callback_data=CoreCB(action=CoreAction.DEPOSIT),
    )

    builder.button(
        text=_("button:back"),
        # icon_custom_emoji_id=Emoji.BACK,
        style=ButtonStyle.DANGER,
        callback_data=CB(action=Action.BACK),
    )

    builder.adjust(2, 1)
    return builder.as_markup()