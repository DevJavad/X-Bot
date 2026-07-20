from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from app.enums import AdminPrefix


class ProductAction(StrEnum):
    BACK = "back"
    EDIT = "edit"
    DELETE = "delete"
    DETAILS = "details"


class ProductCB(CallbackData, prefix=AdminPrefix.PRODUCT):
    action: ProductAction
    product_id: int | None = None