from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from app.enums import Prefix


class PurchaseAction(StrEnum):
    DETAIL = "detail"
    PAGE = "page"
    BACK = "back"
    BUY = "buy"


class PurchaseCB(CallbackData, prefix=Prefix.PURCHASE):
    action: PurchaseAction
    product_id: int | None = None