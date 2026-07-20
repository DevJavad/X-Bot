from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from app.enums import Prefix


class DepositAction(StrEnum):
    CANCEL = "cancel"
    REJECT = "reject"
    CONFIRM = "confirm"


class DepositCB(CallbackData, prefix=Prefix.DEPOSIT):
    action: DepositAction
    invoice_id: str | None = None