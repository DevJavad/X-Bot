import logging

from app.database.models import Invoice, Product, User
from app.enums import InvoiceType, UserRole
from app.settings import Config
from app.utils.constants import PRODUCTS

logger = logging.getLogger(__name__)


async def owner_seed(config: Config) -> None:
    owner_id = config.bot.owner_id

    user, created = await User.get_or_create(
        user_id=owner_id,
        defaults={"role": UserRole.OWNER},
    )

    if created:
        logger.info("Owner created: telegram_id=%s", owner_id)
        return

    if user.role != UserRole.OWNER:
        user.role = UserRole.OWNER
        await user.save(update_fields=["role"])
        logger.info("Existing user promoted to owner: telegram_id=%s", owner_id)
    else:
        logger.info("Owner already exists: telegram_id=%s", owner_id)


async def product_seed() -> None:
    for product in PRODUCTS:
        await Product.get_or_create(
            name=product.get("name"),
            description=product.get("description"),
            traffic=product.get("traffic"),
            user_limit=product.get("user_limit"),
            expires_at=product.get("expires_at"),
            inbound_id=product.get("inbound_id"),
            price=product.get("price"),
        )


async def seed(config: Config) -> None:
    await owner_seed(config)
    await product_seed()