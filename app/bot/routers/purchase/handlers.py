import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from aioxui import XUI

from app.bot.routers.core import CoreAction, CoreCB
from app.database.models import Invoice, Payment, Product, Service, User
from app.enums import InvoiceStatus, InvoiceType, PaymentType, ProductStatus
from app.services.purchase import (
    InsufficientBalanceError,
    ProductNotFoundError,
    PurchaseService,
)

from .buttons import purchase_button, product_detail_button
from .data import PurchaseAction, PurchaseCB

name = __name__
router = Router(name=name)
logger = logging.getLogger(name=name)


@router.callback_query(CoreCB.filter(F.action == CoreAction.PURCHASE))
async def purchase(query: CallbackQuery, user: User) -> None:
    products = await Product.filter(status=ProductStatus.ACTIVE).all()

    if not products:
        return await query.answer(_("notification:products:empty"), True)

    text = _("message:purchase")
    markup = purchase_button(products)
    return await query.message.edit_text(text, reply_markup=markup)


@router.callback_query(PurchaseCB.filter(F.action == PurchaseAction.DETAIL))
async def detail(query: CallbackQuery, callback_data: PurchaseCB, user: User) -> None:
    product = await Product.get_or_none(id=callback_data.product_id, status=ProductStatus.ACTIVE)

    if product is None:
        return await query.answer(_("notification:products:not_found"), True)

    UNLIMITED = _("unit:unlimited")
    traffic = f"{product.traffic} {_("unit:gb")}" if product.traffic else UNLIMITED
    user_limit = f"{product.user_limit} {_("unit:user")}" if product.user_limit else UNLIMITED
    expires_at = f"{product.expires_at} {_("unit:day")}" if product.expires_at else UNLIMITED
    text = _("message:product:detail").format(
        traffic=traffic,
        user_limit=user_limit,
        expires_at=expires_at,
        price=int(product.price),
        description=product.description or "-",
        balance=int(user.balance),
    )
    markup = product_detail_button(product)
    return await query.message.edit_text(text, reply_markup=markup)


@router.callback_query(PurchaseCB.filter(F.action == PurchaseAction.BUY))
async def buy(query: CallbackQuery, callback_data: PurchaseCB, user: User, xui: XUI) -> None:
    try:
        service = await PurchaseService.purchase(user.id, callback_data.product_id, xui)
    except ProductNotFoundError:
        await query.answer(_("notification:products:not_found"), True)
        return
    except InsufficientBalanceError:
        await query.answer(_("notification:balance:insufficient"), True)
        return
    except Exception:
        logger.exception(
            "Unexpected error during purchase: user_id=%s product_id=%s",
            user.id, callback_data.product_id,
        )
        await query.answer(_("notification:purchase:failed"), True)
        return

    text = _("message:purchase:success").format(service_name=service.name)

    await query.answer()
    await query.message.edit_text(text)


@router.callback_query(PurchaseCB.filter(F.action == PurchaseAction.BACK))
async def back_to_purchase_list(query: CallbackQuery, user: User) -> None:
    await purchase(query, user)