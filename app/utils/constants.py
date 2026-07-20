from typing import Any

from aiogram.enums import ChatMemberStatus
from aioxui.enums import UnitType

from app.enums import InvoiceStatus, InvoiceType, Language, ServiceStatus

PACKAGE_ROUTERS: str = "app.bot.routers"

DEFAULT_LANGUAGE: Language = Language.FA

PAYMENT_TIMEOUT: int = 30

UNLIMITED: str = "-"


class DEPOSIT:
    MIN_DEPOSIT: int = 10_000
    MAX_DEPOSIT: int = 1_000_000
    MAX_DAILY_INVOICES: int = 15


class INVOICE:
    PER_PAGE: int = 5
    MAX_FOR_SEARCH: int = 7
    MAX_FOR_FILTER: int = 10


class TRIAL:
    INBOUND_ID: int | list[int] = [2, 3]
    TRAFFIC: int = 500
    TRAFFIC_UNIT = UnitType.MB # TODO: You can use: (UnitType.GB, UnitType.PB, ...)
    EXPIRY: dict[str, int] = {"hours": 12} # TODO: You can use: (days, months, years, ...)
    IP_LIMTI: int = 1
    REWARD: int = 10_000
    GROUP: str | None = None # TODO: You can set group name for trail services


ALLOWED_STATUSES = {
    ChatMemberStatus.MEMBER,
    ChatMemberStatus.CREATOR,
    ChatMemberStatus.ADMINISTRATOR,
}

INVOICE_TYPE_MAP: dict[str, str] = {
    InvoiceType.RENEWAL: "تمدید سرویس",
    InvoiceType.DEPOSIT: "افزایش موجودی",
    InvoiceType.PURCHASE: "خرید سرویس",
}

INVOICE_STATUS_MAP: dict[str, str] = {
    InvoiceStatus.PAID: "پرداخت شده ✅",
    InvoiceStatus.PENDING: "در انتظار تایید ⏳",
    InvoiceStatus.EXPIRED: "منقضی شده ⏳",
    InvoiceStatus.REJECTED: "رد شده ⚠️",
    InvoiceStatus.CANCELLED: "کنسل شده ❌",
}

SERVICE_STATUS_MAP: dict[str, str] = {
    ServiceStatus.ACTIVE: "فعال ✅",
    ServiceStatus.INACTIVE: "غیرفعال ❌",
    ServiceStatus.EXPIRED: "منقضی ⏳",
    ServiceStatus.SUSPENDED: "تعلیق‌ ⚠️",
}


PRODUCTS: list[dict[str, Any]] = [
    {
        "name": "نامحدود 1 ماهه تک کاربره",
        "description": "پینگ ثابت و سرعت پایدار - لوکیشن آلمان - بدون مصرف منصفانه",
        "traffic": 0,
        "user_limit": 1,
        "expires_at": 30,
        "inbound_id": [2, 3],
        "price": 120_000,
    },
    {
        "name": "نامحدود 1 ماهه دو کاربره",
        "description": "پینگ ثابت و سرعت پایدار - لوکیشن آلمان - بدون مصرف منصفانه",
        "traffic": 0,
        "user_limit": 2,
        "expires_at": 30,
        "inbound_id": [2, 3],
        "price": 200_000,
    },
]