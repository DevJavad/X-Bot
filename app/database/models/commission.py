from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise.fields import DecimalField, ForeignKeyField, ForeignKeyRelation, IntField

from app.database.models import BaseModel

if TYPE_CHECKING:
    from app.database.models import Invite, Payment


class Commission(BaseModel):
    invite: ForeignKeyRelation[Invite] = ForeignKeyField("models.Invite", "commissions")
    payment: ForeignKeyRelation[Payment] = ForeignKeyField("models.Payment", "commissions", unique=True)

    amount = DecimalField(max_digits=12, decimal_places=2)
    percent = IntField(default=0)

    class Meta:
        table = "commissions"