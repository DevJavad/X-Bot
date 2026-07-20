from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from app.enums import Prefix


class AdminAction(StrEnum):
    PRODUCTS = "products"


class AdminCB(CallbackData, prefix=Prefix.ADMIN):
    action: AdminAction