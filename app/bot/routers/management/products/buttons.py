from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


from app.bot.routers.core import BackAction, BackCB
from app.database.models import Product

from .data import ProductAction as Action, ProductCB as CB


def products_button(products: list[Product]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for product in products:
        builder.button(
            text=f"{product.name} - {int(product.price):,}",
            style=ButtonStyle.PRIMARY,
            callback_data=CB(action=Action.DETAILS, product_id=product.id),
        )
    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(
            text=_("button:back"),
            # icon_custom_emoji_id=Emoji.BACK,
            style=ButtonStyle.DANGER,
            callback_data=BackCB(action=BackAction.MANAGEMENT).pack(),
        )
    )
    return builder.as_markup()