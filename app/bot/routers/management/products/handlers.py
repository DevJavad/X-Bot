import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from app.bot.routers.management import AdminAction as Action, AdminCB as CB
from app.database.models import Product
from app.enums import ProductStatus

from .buttons import products_button

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.callback_query(CB.filter(F.action == Action.PRODUCTS))
async def products(query: CallbackQuery):
    products = await Product.filter(status=ProductStatus.ACTIVE)

    if not products:
        return await query.answer(_("notification:products:empty"), True)

    return await query.message.edit_text(
        _("message:management:products"),
        reply_markup=products_button(products),
    )