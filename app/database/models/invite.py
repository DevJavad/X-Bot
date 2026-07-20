from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise.fields import ForeignKeyField, ForeignKeyRelation

from app.database.models import BaseModel

if TYPE_CHECKING:
    from app.database.models import User


class Invite(BaseModel):
    inviter: ForeignKeyRelation[User] = ForeignKeyField("models.User", "sent_invites")
    invited: ForeignKeyRelation[User] = ForeignKeyField("models.User", "received_invites")

    class Meta:
        table = "invites"