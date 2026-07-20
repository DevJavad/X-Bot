import asyncio
import logging

from app.core import bootstrap

logger = logging.getLogger(__name__)


async def main():
    app = await bootstrap()

    try:
        await app.dp.start_polling(app.bot)

    finally:
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())