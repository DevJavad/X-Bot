from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from tortoise.fields import (
    CharEnumField,
    CharField,
    DatetimeField,
    DecimalField,
    ForeignKeyField,
    ForeignKeyRelation,
)
from tortoise.timezone import now

from app.database.models import BaseModel
from app.enums import InvoiceStatus, InvoiceType
from app.utils.constants import PAYMENT_TIMEOUT
from app.utils.functions import uuid

if TYPE_CHECKING:
    from app.database.models import User


class Invoice(BaseModel):
    user: ForeignKeyRelation[User] = ForeignKeyField("models.User", "invoices")

    invoice_id = CharField(max_length=32, unique=True, default=lambda: uuid().hex[:16])

    receipt_photo_id = CharField(max_length=255, unique=True, null=True)

    amount = DecimalField(max_digits=12, decimal_places=2)
    discount = DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = DecimalField(max_digits=12, decimal_places=2)

    type = CharEnumField(InvoiceType)
    status = CharEnumField(InvoiceStatus, default=InvoiceStatus.PENDING)

    description = CharField(max_length=255, null=True)

    payment_datetime = DatetimeField(null=True)

    expires_at = DatetimeField(default=lambda: now() + timedelta(minutes=PAYMENT_TIMEOUT))

    class Meta:
        table = "invoices"

    async def confirm_payment(self):
        self.status = InvoiceStatus.PAID
        self.payment_datetime = now()
        await self.save()