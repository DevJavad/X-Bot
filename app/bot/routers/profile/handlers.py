import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from app.bot.routers.core import back_button, BackAction, CoreCB, CoreAction
from app.database.models import Payment, Invoice, Service, User, Invite
from app.utils.datetime import to_jalali

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.callback_query(CoreCB.filter(F.action == CoreAction.PROFILE))
async def profile(query: CallbackQuery, user: User):
    invoices = await Invoice.filter(user=user).count()
    payments = await Payment.filter(user=user).count()
    services = await Service.filter(user=user).count()
    invites = await Invite.filter(inviter_id=user.id).count()

    return await query.message.edit_text(
        _("message:profile").format(
            invites=invites,
            invoices=invoices,
            payments=payments,
            services=services,
            balance=int(user.balance),
            user_id=user.user_id,
            join_date=to_jalali(user.created_at),
        ),
        reply_markup=back_button(BackAction.MAIN),
    )