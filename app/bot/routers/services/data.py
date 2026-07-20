from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from app.enums import Prefix


class ServiceAction(StrEnum):
    DETAILS = "detail"
    PAGE = "page"
    BACK = "back"
    NEXT = "next"
    PREVIOUS = "previous"


class ServiceCB(CallbackData, prefix=Prefix.SERVICES):
    action: ServiceAction
    service_id: int | None = None
    page: int | None = None