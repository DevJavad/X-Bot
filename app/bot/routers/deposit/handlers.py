import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _

from app.bot.routers.core import BackAction, back_button, start_button, CoreAction, CoreCB

from app.database.models import Invoice, Payment, User
from app.enums import InvoiceStatus, InvoiceType, PaymentType
from app.settings import Config
from app.utils.constants import DEPOSIT, INVOICE_STATUS_MAP, INVOICE_TYPE_MAP
from app.utils.datetime import today_range
from app.utils.states import DepositState

from .buttons import deposit_button, confirm_button
from .data import DepositAction, DepositCB

name = __name__

router = Router(name=name)
logger = logging.getLogger(name=name)


@router.callback_query(CoreCB.filter(F.action == CoreAction.DEPOSIT))
async def deposit(query: CallbackQuery, state: FSMContext, user: User):
    start, end = today_range()

    count = await Invoice.filter(
        user=user,
        type=InvoiceType.DEPOSIT,
        created_at__gte=start,
        created_at__lt=end,
    ).count()

    if count >= DEPOSIT.MAX_DAILY_INVOICES:
        return await query.answer(
            _("notification:deposit:limit").format(limit=DEPOSIT.MAX_DAILY_INVOICES),
            True,
        )

    pending_invoice = await Invoice.filter(
        user=user,
        type=InvoiceType.DEPOSIT,
        status=InvoiceStatus.PENDING,
    ).first()
    if pending_invoice:
        return await query.answer(_("notification:deposit:pending_exists"), True)

    await state.set_state(DepositState.amount)

    text = _("message:deposit").format(
        limit=DEPOSIT.MAX_DAILY_INVOICES,
        min=DEPOSIT.MIN_DEPOSIT,
        max=DEPOSIT.MAX_DEPOSIT,
    )
    markup = back_button(BackAction.MAIN)

    return await query.message.edit_text(text, reply_markup=markup)


@router.message(DepositState.amount, F.text)
async def amount(
    message: Message,
    state: FSMContext,
    user: User,
    config: Config,
):
    amount = message.text

    if not amount.isdigit():
        text = _("message:deposit:invalid_value")
        markup = back_button(BackAction.MAIN)

        return await message.answer(text, reply_markup=markup)

    amount = int(amount)

    if not (DEPOSIT.MIN_DEPOSIT <= amount <= DEPOSIT.MAX_DEPOSIT):
        text = _("message:deposit:invalid_number").format(
            min=DEPOSIT.MIN_DEPOSIT, max=DEPOSIT.MAX_DEPOSIT
        )
        markup = back_button(BackAction.MAIN)

        return await message.answer(text, reply_markup=markup)

    invoice = await Invoice.create(
        user=user,
        amount=amount,
        final_amount=amount,
        type=InvoiceType.DEPOSIT,
    )

    await state.set_state(DepositState.pending)
    await state.update_data(invoice_id=invoice.invoice_id)

    text = _("message:deposit:invoice").format(
        invoice_id=invoice.invoice_id,
        amount=amount,
        type=INVOICE_TYPE_MAP.get(invoice.type),
    )
    markup = deposit_button(config)

    return await message.answer(text, reply_markup=markup)


@router.message(DepositState.pending, F.photo)
async def pending(
    message: Message,
    state: FSMContext,
    user: User,
    config: Config,
):
    data = await state.get_data()
    invoice_id = data.get("invoice_id")

    if invoice_id:
        invoice = await Invoice.get_or_none(
            user=user,
            invoice_id=invoice_id,
            status=InvoiceStatus.PENDING,
        )
        if invoice.receipt_photo_id:
            return await message.answer(_("message:deposit:receipt_already_sent"))

        photo = message.photo[-1]

        updated_count = await Invoice.filter(
            id=invoice.id,
            receipt_photo_id__isnull=True,
        ).update(receipt_photo_id=photo.file_id)

        if updated_count == 0:
            return await message.answer(_("message:deposit:receipt_already_sent"))

        if invoice:
            photo = message.photo[-1]
            invoice.receipt_photo_id = photo.file_id
            await invoice.save()

            await state.set_state(DepositState.confirming)

            caption = _("message:deposit:confirming").format(
                type=INVOICE_TYPE_MAP.get(invoice.type),
                invoice_id=invoice_id,
                amount=int(invoice.amount),
                user_id=user.user_id,
                username=f"@{user.username}" if user.username else "-",
                status=INVOICE_STATUS_MAP.get(invoice.status),
                receipt_photo_id=invoice.receipt_photo_id,
            )
            markup = confirm_button(invoice_id)

            await message.copy_to(
                config.bot.owner_id,
                caption=caption,
                reply_markup=markup,
            )

            text = _("message:deposit:wait")
            button = back_button(BackAction.MAIN)
            return await message.answer(text, reply_markup=button)


@router.callback_query(DepositCB.filter(F.action == DepositAction.CANCEL))
async def cancel(query: CallbackQuery, user: User, state: FSMContext):
    data = await state.get_data()
    invoice_id = data.get("invoice_id")

    if invoice_id:
        invoice = await Invoice.get_or_none(
            user=user,
            invoice_id=invoice_id,
            status=InvoiceStatus.PENDING,
        )
        if invoice:
            invoice.status = InvoiceStatus.CANCELLED
            await invoice.save()
            logger.info(
                "A user canceled an invoice | user_id=%s invoice_id=%s",
                user.user_id,
                invoice_id,
            )

    await state.clear()

    await query.answer(_("notification:invoice:cancel"))

    text = _("message:start").format(name=query.message.from_user.full_name)
    markup = start_button(user.role)

    return await query.message.edit_text(text, reply_markup=markup)


@router.callback_query(DepositCB.filter(F.action == DepositAction.CONFIRM))
async def confirm(query: CallbackQuery, callback_data: DepositCB, user: User):
    invoice_id = callback_data.invoice_id

    invoice = await Invoice.get_or_none(
        invoice_id=invoice_id, status=InvoiceStatus.PENDING
    )
    if invoice:
        await invoice.confirm_payment()
        await invoice.save()

        user = await invoice.user

        previous_balance = user.balance
        current_balance = previous_balance + invoice.amount

        user.balance = current_balance
        await user.save()

        payment = await Payment.create(
            user=user,
            invoice=invoice,
            amount=invoice.amount,
            previous_balance=previous_balance,
            current_balance=current_balance,
            type=PaymentType.DEPOSIT,
        )

        caption = _("message:deposit:confirming").format(
            type=INVOICE_TYPE_MAP.get(invoice.type),
            invoice_id=invoice_id,
            amount=int(invoice.amount),
            user_id=user.user_id,
            username=f"@{user.username}" if user.username else "-",
            status=INVOICE_STATUS_MAP.get(invoice.status),
            receipt_photo_id=invoice.receipt_photo_id,
        )
        await query.message.edit_caption(caption=caption)
        await query.answer(_("notification:deposit:confirm"), True)

        text = _("message:deposit:confirm").format(
            invoice_id=invoice_id,
            amount=int(invoice.amount),
        )
        markup = back_button(BackAction.MAIN)
        user = await invoice.user
        return await query.bot.send_message(user.user_id, text, reply_markup=markup)


@router.callback_query(DepositCB.filter(F.action == DepositAction.REJECT))
async def confirm(query: CallbackQuery, callback_data: DepositCB, user: User):
    invoice_id = callback_data.invoice_id

    invoice = await Invoice.get_or_none(
        invoice_id=invoice_id, status=InvoiceStatus.PENDING
    )
    if invoice:
        invoice.status = InvoiceStatus.REJECTED
        await invoice.save()

        caption = _("message:deposit:confirming").format(
            type=INVOICE_TYPE_MAP.get(invoice.type),
            invoice_id=invoice_id,
            amount=int(invoice.amount),
            user_id=user.user_id,
            username=f"@{user.username}" if user.username else "-",
            status=INVOICE_STATUS_MAP.get(invoice.status),
            receipt_photo_id=invoice.receipt_photo_id,
        )
        await query.message.edit_caption(caption=caption)
        await query.answer(_("notification:deposit:reject"), True)

        text = _("message:deposit:reject").format(
            invoice_id=invoice_id,
            amount=int(invoice.amount),
        )
        markup = back_button(BackAction.MAIN)
        user = await invoice.user
        return await query.bot.send_message(user.user_id, text, reply_markup=markup)
