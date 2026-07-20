import logging
import os
import subprocess
from dataclasses import dataclass

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties as Default
from aiogram.enums import ChatType, ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n
from aioxui import XUI

from app.bot.middlewares import (
    DBI18nMiddleware,
    LocaleMiddleware,
    MembershipMiddleware,
    ThrottlingMiddleware,
    UserMiddleware,
)
from app.database import Database, Redis
from app.enums import DatabaseDriver as Driver
from app.settings import Config, BASE_DIR, setup_logger, include_routers
from app.utils.constants import DEFAULT_LANGUAGE, PACKAGE_ROUTERS
from app.core.seed import seed

logger = logging.getLogger(__name__)

LOCALES: str = "locales"


@dataclass
class App:
    config: Config
    xui: XUI
    redis: Redis
    database: Database
    i18n: I18n
    bot: Bot
    dp: Dispatcher

    async def shutdown(self) -> None:
        await self.xui.stop()
        await self.redis.close()
        await self.database.disconnect()


async def bootstrap() -> App:
    subprocess.run(["pybabel", "compile", "-d", "app/locales"])

    config = Config()

    setup_logger(config)

    locale_path = os.path.join(BASE_DIR, LOCALES)
    i18n = I18n(path=locale_path, default_locale=DEFAULT_LANGUAGE)
    i18n.set_current(i18n)

    xui = XUI(config.xui.base_url, config.xui.token)
    await xui.start()

    redis = Redis(config.redis.url)
    await redis.init()

    database = Database(config.database.url(Driver.SQLITE))
    await database.connect()

    await seed(config)

    bot = Bot(config.bot.token, default=Default(parse_mode=ParseMode.HTML))

    dp = Dispatcher(
        config=config,
        xui=xui,
        redis=redis,
        storage=RedisStorage(redis.client),
    )

    routers = include_routers(dp, PACKAGE_ROUTERS)
    logger.info("Include routers: %s", routers)

    dp.message.filter(F.chat.type == ChatType.PRIVATE)
    dp.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(UserMiddleware())
    dp.message.middleware(LocaleMiddleware())
    dp.message.middleware(DBI18nMiddleware(i18n))
    dp.message.middleware(MembershipMiddleware())

    dp.callback_query.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    dp.callback_query.middleware(LocaleMiddleware())
    dp.callback_query.middleware(DBI18nMiddleware(i18n))
    dp.callback_query.middleware(MembershipMiddleware())

    return App(config, xui, redis, database, i18n, bot, dp)