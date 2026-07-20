import logging
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _

from app.bot.routers.core import CoreAction, join_button
from app.settings import Config
from app.utils.functions import is_member

logger = logging.getLogger(__name__)


class MembershipMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:

        if isinstance(event, Message) and event.text and event.text.startswith("/start"):
            return await handler(event, data)

        if isinstance(event, CallbackQuery) and event.data == CoreAction.JOINED:
            return await handler(event, data)

        config: Config = data["config"]

        if await is_member(event.bot, config, event.from_user.id):
            return await handler(event, data)

        text = _("message:join_required")
        markup = join_button(config)

        message = event if isinstance(event, Message) else event.message
        return await message.edit_text(text, reply_markup=markup)