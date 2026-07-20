import logging

from aioxui import XUI
from aioxui.models import Client
from tortoise.transactions import in_transaction

from app.database.models import Invoice, Payment, Product, Service, User
from app.enums import InvoiceStatus, InvoiceType, PaymentType, ProductStatus

logger = logging.getLogger(__name__)


class InsufficientBalanceError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class PurchaseService:
    @staticmethod
    async def purchase(user_id: int, product_id: int, xui: XUI) -> Service:
        async with in_transaction() as conn:
            product = (
                await Product.filter(
                    id=product_id,
                    status=ProductStatus.ACTIVE,
                )
                .using_db(conn)
                .first()
            )
            if product is None:
                raise ProductNotFoundError(
                    f"Product not found or inactive: {product_id}"
                )

            user = await User.select_for_update().using_db(conn).get(id=user_id)
            if user.balance < product.price:
                raise InsufficientBalanceError(
                    f"Insufficient balance: balance={user.balance}, price={product.price}"
                )

            previous_balance = user.balance
            new_balance = previous_balance - product.price

            invoice = await Invoice.create(
                using_db=conn,
                user=user,
                amount=product.price,
                final_amount=product.price,
                type=InvoiceType.PURCHASE,
                status=InvoiceStatus.PAID,
                description=product.name
            )

            await Payment.create(
                using_db=conn,
                user=user,
                invoice=invoice,
                amount=product.price,
                previous_balance=previous_balance,
                current_balance=new_balance,
                type=PaymentType.PURCHASE,
            )

            await User.filter(id=user_id).using_db(conn).update(balance=new_balance)

            input = Client(
                totalGB=product.traffic,
                expiryTime=product.expires_at,
                limitIp=product.user_limit,
                tgId=user_id,
            )
            client = await xui.client.add(product.inbound_id, input)

            service = await Service.create(
                using_db=conn,
                user=user,
                product=product,
                invoice=invoice,
                inbound_id=product.inbound_id,
                uuid=client.uuid,
                name=client.email,
                sub_id=client.sub_id,
                group=client.group,
                traffic_limit=client.traffic_limit,
                user_limit=client.ip_limit
            )

            logger.info(
                "Purchase completed: user_id=%s product_id=%s invoice_id=%s service_id=%s",
                user_id,
                product_id,
                invoice.invoice_id,
                service.id,
            )

            return service