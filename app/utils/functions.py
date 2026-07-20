import logging
from io import BytesIO
from uuid import UUID, uuid4

import qrcode
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from app.settings import Config
from app.utils.constants import ALLOWED_STATUSES

logger = logging.getLogger(__name__)


async def is_member(bot: Bot, config: Config, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=f"@{config.bot.channel_username}",
            user_id=user_id,
        )
        return member.status in ALLOWED_STATUSES

    except TelegramAPIError as e:
        logger.warning("Membership check failed for user_id=%s: %s", user_id, e)
        return False


def uuid() -> UUID:
    return uuid4()


def generate_qrcode(config: str) -> bytes:
    buffer = BytesIO()
    image = qrcode.make(config)
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()