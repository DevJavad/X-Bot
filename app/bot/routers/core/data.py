from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from app.enums import Prefix


class CoreAction(StrEnum):
    PURCHASE = "purchase"
    RENEWAL = "renewal"

    DEPOSIT = "deposit"
    PROFILE = "profile"

    SERVICES = "services"
    INVOICES = "invoices"

    TRIAL = "trial"
    INVITE = "invite"

    SUPPORT = "support"
    TUTORIAL = "tutorial"

    MANAGEMENT = "management"

    JOINED = "joined"


class CoreCB(CallbackData, prefix=Prefix.CORE):
    action: CoreAction


class BackAction(StrEnum):
    MAIN = "main"
    PURCHASE = "purchase"
    MANAGEMENT = "management"


class BackCB(CallbackData, prefix=Prefix.BACK):
    action: BackAction