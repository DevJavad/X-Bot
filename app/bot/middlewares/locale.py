from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n.middleware import I18nMiddleware

from app.database.models import User
from app.enums import Language
from app.utils.constants import DEFAULT_LANGUAGE


class LocaleMiddleware(BaseMiddleware):
    def __init__(self, default_language: Language = DEFAULT_LANGUAGE):
        self.default_language = default_language

    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ):
        user: User = data.get("user")
        data["locale"] = user.language if user else self.default_language

        return await handler(event, data)


class DBI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event, data: dict[str, Any]):
        return data.get("locale", DEFAULT_LANGUAGE)