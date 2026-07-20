import importlib
import pkgutil
from pathlib import Path
from typing import Optional

from aiogram import Dispatcher
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.enums import DatabaseDriver

BASE_DIR = Path(__file__).resolve().parent.parent


class BotConfig(BaseModel):
    token: str
    owner_id: int
    channel_username: str


class XUIConfig(BaseModel):
    host: str
    port: int
    path: str

    token: str

    subscription_port: int | None = None
    subscription_path: str
    subscription_host: str

    @property
    def base_url(self) -> str:
        return f"{self.host}:{self.port}/{self.path}"

    def subscription_url(self, sub_id: str) -> str:
        if self.subscription_port:
            return f"{self.subscription_host}:{self.subscription_port}/{self.subscription_path}/{sub_id}"

        return f"{self.subscription_host}/{self.subscription_path}/{sub_id}"


class PaymentConfig(BaseModel):
    card_number: str


class DatabaseConfig(BaseModel):
    name: str
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None

    def url(self, driver: DatabaseDriver) -> str:
        if driver in (DatabaseDriver.SQLITE, DatabaseDriver.SQLITE_AIOSQLITE):
            return f"{driver.value}://app/{self.name}.sqlite"

        return f"{driver.value}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisConfig(BaseModel):
    host: str
    port: int

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"


class LoggerConfig(BaseModel):
    level: str
    enabled: bool


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    bot: BotConfig
    xui: XUIConfig
    payment: PaymentConfig
    database: DatabaseConfig
    redis: RedisConfig
    logger: LoggerConfig


def include_routers(dp: Dispatcher, package: str) -> int:
    count = 0
    module = importlib.import_module(package)

    for _, name, is_package in pkgutil.iter_modules(module.__path__):
        full_name = f"{package}.{name}"
        sub_module = importlib.import_module(full_name)

        if hasattr(sub_module, "router"):
            router = sub_module.router
            dp.include_router(router)

            count += sum(
                len(observer.handlers) for observer in router.observers.values()
            )

        if is_package:
            count += include_routers(dp, full_name)

    return count
