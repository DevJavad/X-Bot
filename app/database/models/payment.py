from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise.fields import (
    CharEnumField,
    DecimalField,
    ForeignKeyField,
    ForeignKeyRelation,
)

from app.database.models import BaseModel
from app.enums import PaymentType

if TYPE_CHECKING:
    from app.database.models import Invoice, User


class Payment(BaseModel):
    user: ForeignKeyRelation[User] = ForeignKeyField("models.User", "payments")
    invoice: ForeignKeyRelation[Invoice] = ForeignKeyField("models.Invoice", "payments")

    amount = DecimalField(max_digits=12, decimal_places=2)

    previous_balance = DecimalField(max_digits=12, decimal_places=2)
    current_balance = DecimalField(max_digits=12, decimal_places=2)

    type = CharEnumField(PaymentType)

    class Meta:
        table = "payments"