from enum import StrEnum


class Prefix(StrEnum):
    BACK = "back"
    CORE = "core"
    DEPOSIT = "deposit"
    INVOICE = "invoice"
    PURCHASE = "purchase"
    SERVICES = "services"
    ADMIN = "admin"
    
    
class AdminPrefix(StrEnum):
    PRODUCT = "product"
    BACK = "back"
    CORE = "core"
    DEPOSIT = "deposit"
    INVOICE = "invoice"
    PURCHASE = "purchase"
    SERVICES = "services"
    ADMIN = "admin"