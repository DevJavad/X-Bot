from tortoise.fields import (
    BigIntField,
    BooleanField,
    CharEnumField,
    CharField,
    DecimalField,
)

from app.database.models import BaseModel
from app.enums import Language, UserRole, UserStatus
from app.utils.constants import DEFAULT_LANGUAGE
from app.utils.functions import uuid


class User(BaseModel):
    user_id = BigIntField(unique=True)
    username = CharField(max_length=64, null=True)
    phone_number = CharField(max_length=20, null=True)

    language = CharEnumField(Language, default=DEFAULT_LANGUAGE)

    balance = DecimalField(max_digits=12, decimal_places=2, default=0)
    invite_code = CharField(max_length=32, unique=True, default=lambda: uuid().hex[:8])

    role = CharEnumField(UserRole, default=UserRole.USER)
    status = CharEnumField(UserStatus, default=UserStatus.ACTIVE)

    trial_used = BooleanField(default=False)

    class Meta:
        table = "users"