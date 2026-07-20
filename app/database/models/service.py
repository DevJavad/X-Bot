from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise.fields import (
    BigIntField,
    CharEnumField,
    CharField,
    ForeignKeyField,
    ForeignKeyRelation,
    IntField,
    JSONField,
)

from app.database.models import BaseModel
from app.database.models.product import Product
from app.enums import ServiceStatus

if TYPE_CHECKING:
    from app.database.models import Invoice, Product, User


class Service(BaseModel):
    user: ForeignKeyRelation[User] = ForeignKeyField("models.User", "services")
    
    product: ForeignKeyRelation[Product] = ForeignKeyField(
        "models.Product",
        "services",
        null=True,
    )
    invoice: ForeignKeyRelation[Invoice] = ForeignKeyField(
        "models.Invoice",
        "services",
        null=True,
    )

    inbound_id = JSONField(default=list)

    uuid = CharField(max_length=64, unique=True)
    name = CharField(max_length=100, unique=True)
    sub_id = CharField(max_length=64, unique=True)

    group = CharField(max_length=64, null=True)

    traffic_limit = BigIntField(default=0)
    traffic_used = BigIntField(default=0)

    user_limit = IntField(default=0)
    expire_time = BigIntField(default=0)

    status = CharEnumField(ServiceStatus, default=ServiceStatus.ACTIVE)

    class Meta:
        table = "services"
