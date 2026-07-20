from enum import StrEnum


class InvoiceStatus(StrEnum):
    PAID = "paid"
    PENDING = "pending"
    EXPIRED = "expired"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class InvoiceType(StrEnum):
    RENEWAL = "renewal"
    DEPOSIT = "deposit"
    PURCHASE = "purchase"