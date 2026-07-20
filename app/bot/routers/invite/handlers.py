import logging
from decimal import Decimal

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from tortoise.functions import Sum

from app.bot.routers.core import CoreCB, CoreAction
from app.database.models import User, Commission, Invite

from .buttons import invite_button

router = Router(name=__name__)
logger = logging.getLogger(__name__)


async def get_invite_stats(user_id: int) -> dict:
    invites = await Invite.filter(inviter_id=user_id).count()
    buys = await Commission.filter(invite__inviter_id=user_id).count()

    result = (
        await Commission.filter(invite__inviter_id=user_id)
        .annotate(total=Sum("amount"))
        .first()
        .values("total")
    )
    buy_balance = (result or {}).get("total") or Decimal("0")

    return invites, buys, buy_balance


@router.callback_query(CoreCB.filter(F.action == CoreAction.INVITE))
async def invite_link(query: CallbackQuery, user: User):
    bot = await query.bot.get_me()
    link: str = f"https://t.me/{bot.username}?start={user.invite_code}"

    invites, buys, buy_balance = await get_invite_stats(user.user_id)
    return await query.message.edit_text(
        _("message:invite").format(
            invites=invites,
            buys=buys,
            buy_balance=buy_balance,
        ),
        reply_markup=invite_button(link),
    )