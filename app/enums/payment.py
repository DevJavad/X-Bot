from enum import StrEnum


class PaymentType(StrEnum):
    DEPOSIT = "deposit"
    PURCHASE = "purchase"
    REFUND = "refund"
    BONUS = "bonus"