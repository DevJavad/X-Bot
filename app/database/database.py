import logging

import redis.asyncio as redis
from tortoise import Tortoise

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, url: str):
        self.url = url
        self.driver = url.split(":")[0]

    async def connect(self) -> None:
        await Tortoise.init(db_url=self.url, modules={"models": ["app.database.models"]})
        await Tortoise.generate_schemas()
        logger.info("Database connected: [%s] %s", self.driver, self.url)

    async def disconnect(self) -> None:
        await Tortoise.close_connections()
        logger.info("Database disconnected: [%s] %s", self.driver, self.url)


class Redis:
    def __init__(self, url: str):
        self.url = url
        self.client: redis.Redis | None = None

    async def init(self):
        self.client = redis.from_url(self.url, decode_responses=False)
        await self.client.ping()
        logger.info("Start redis service on: %s", self.url)

    async def close(self):
        if self.client:
            await self.client.close()
            logger.info("Stop redis service on: %s", self.url)