from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from app.settings import Config


class IsOwner(BaseFilter):
    async def __call__(self, event: TelegramObject, config: Config) -> bool:
        user = getattr(event, "from_user", None)

        return user is not None and user.id == config.bot.owner_id