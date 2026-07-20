import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from app.database.models import User
from app.bot.filters import IsOwner

from app.bot.routers.core import CoreAction as Action, CoreCB as CB

from .buttons import management_button

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.callback_query(CB.filter(F.action == Action.MANAGEMENT), IsOwner())
async def management(query: CallbackQuery, user: User):
    return await query.message.edit_text(
        _("message:management").format(admin_id=user.user_id),
        reply_markup=management_button(),
    )