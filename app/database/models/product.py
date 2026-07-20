from tortoise.fields import (
    BigIntField,
    CharEnumField,
    CharField,
    DecimalField,
    IntField,
    JSONField,
)

from app.database.models import BaseModel
from app.enums import ProductStatus


class Product(BaseModel):
    name = CharField(max_length=64)
    description = CharField(max_length=255, null=True)

    traffic = BigIntField(default=0)
    user_limit = IntField(default=0)
    inbound_id = JSONField(default=list)
    expires_at = IntField(default=0)

    price = DecimalField(max_digits=12, decimal_places=2)
    status = CharEnumField(ProductStatus, default=ProductStatus.ACTIVE)

    class Meta:
        table = "products"