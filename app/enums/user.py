from enum import StrEnum


class UserRole(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    SUPER_USER = "super_user"
    USER = "user"


class UserStatus(StrEnum):
    ACTIVE = "active"
    BANNED = "banned"


class Language(StrEnum):
    FA = "fa"
    EN = "en"
    RU = "ru"
    ZH = "zh"