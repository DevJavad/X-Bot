import logging
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from app.database.models import Invite, User

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        user, is_new_user = await User.get_or_create(
            user_id=user_id,
            defaults={"username": event.from_user.username},
        )

        if is_new_user:
            logger.info("Created a new user: %s", user_id)

            if isinstance(event, Message) and event.text and event.text.startswith("/start"):
                args = event.text.removeprefix("/start").strip()
                if args:
                    await self.set_inviter(user, args)

        data["user"] = user
        data["is_new_user"] = is_new_user

        return await handler(event, data)

    @staticmethod
    async def set_inviter(user: User, invite_code: str) -> None:
        inviter = await User.get_or_none(invite_code=invite_code)

        if inviter is None or inviter.id == user.id:
            return

        await Invite.create(inviter=inviter, invited=user)
        logger.info(
            "Invite recorded: inviter=%s invited=%s", inviter.user_id, user.user_id
        )