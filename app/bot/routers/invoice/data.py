from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from app.enums import Prefix


class InvoiceAction(StrEnum):
    DETAIL = "detail"
    PAGE = "page"
    BACK = "back"
    CANCEL = "cancel"


class InvoiceCB(CallbackData, prefix=Prefix.INVOICE):
    action: InvoiceAction
    invoice_id: str | None = None
    page: int | None = None