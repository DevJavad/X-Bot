import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from aioxui import XUI
from aioxui.enums import Calendar
from aioxui.utils import DateTime, Storage

from app.settings import Config
from app.bot.routers.core import CoreAction, CoreCB
from app.database.models import Service, User
router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.callback_query(CoreCB.filter(F.action == CoreAction.TUTORIAL))
async def tutorial(query: CallbackQuery, user: User):
    ...