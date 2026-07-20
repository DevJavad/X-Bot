from typing import Any, Callable, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from app.database import Redis


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, delay: int = 1):
        self.delay = delay

    async def __call__(
        self,
        handler: Callable,
        event: Union[Message, CallbackQuery],
        data: dict[str, Any],
    ):
        redis: Redis = data["redis"]

        result = await redis.client.set(f"spam:{event.from_user.id}", "1", ex=self.delay, nx=True)
        if not result:
            return

        return await handler(event, data)