from tortoise.fields import BigIntField, DatetimeField
from tortoise.models import Model


class BaseModel(Model):
    id = BigIntField(pk=True)

    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)

    class Meta:
        abstract = True