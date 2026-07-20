import logging
from math import ceil

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from app.bot.routers.core import CoreAction, CoreCB
from app.database.models import Invoice, User
from app.utils.constants import INVOICE, INVOICE_STATUS_MAP, INVOICE_TYPE_MAP
from app.utils.datetime import today_range

from .buttons import invoices_button, invoice_detail_button
from .data import InvoiceAction, InvoiceCB

name = __name__
router = Router(name=name)
logger = logging.getLogger(name=name)


async def render_invoices(
    query: CallbackQuery,
    state: FSMContext,
    user: User,
    page: int = 0,
) -> None:
    count = await Invoice.filter(user=user).count()

    if count < 1:
        await query.answer(_("notification:invoices:empty"), True)
        return

    start, end = today_range()
    today = await Invoice.filter(
        user=user,
        created_at__gte=start,
        created_at__lt=end,
    ).count()

    pages = ceil(count / INVOICE.PER_PAGE) if count > 0 else 1

    invoice_list = (
        await Invoice.filter(user=user)
        .order_by("-created_at")
        .offset(page * INVOICE.PER_PAGE)
        .limit(INVOICE.PER_PAGE)
    )

    await state.update_data(invoice_page=page)

    text = _("message:invoices:list").format(
        count=count,
        today=today,
        page=page + 1,
        pages=pages,
    )
    markup = invoices_button(invoice_list, page, pages)

    return await query.message.edit_text(text, reply_markup=markup)


@router.callback_query(CoreCB.filter(F.action == CoreAction.INVOICES))
async def show_invoices(query: CallbackQuery, state: FSMContext, user: User) -> None:
    await render_invoices(query, state, user)


@router.callback_query(InvoiceCB.filter(F.action == InvoiceAction.PAGE))
async def paginate_invoices(
    query: CallbackQuery,
    callback_data: InvoiceCB,
    state: FSMContext,
    user: User,
) -> None:
    await render_invoices(query, state, user, page=callback_data.page or 0)


@router.callback_query(InvoiceCB.filter(F.action == InvoiceAction.DETAIL))
async def show_invoice_detail(
    query: CallbackQuery,
    callback_data: InvoiceCB,
    user: User,
) -> None:
    invoice = await Invoice.get_or_none(invoice_id=callback_data.invoice_id, user=user)

    text = _("message:invoice:detail").format(
        invoice_id=invoice.invoice_id,
        type=INVOICE_TYPE_MAP.get(invoice.type),
        status=INVOICE_STATUS_MAP.get(invoice.status),
        amount=int(invoice.amount),
        discount=int(invoice.discount),
        final_amount=int(invoice.final_amount),
        description=invoice.description or "-",
        receipt_photo_id=invoice.receipt_photo_id,
    )
    return await query.message.edit_text(text, reply_markup=invoice_detail_button())


@router.callback_query(InvoiceCB.filter(F.action == InvoiceAction.BACK))
async def back_to_invoice_list(
    query: CallbackQuery,
    state: FSMContext,
    user: User,
) -> None:
    data = await state.get_data()
    await render_invoices(query, state, user, page=data.get("invoice_page", 0))
