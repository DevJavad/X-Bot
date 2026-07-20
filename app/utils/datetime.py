from datetime import datetime, timedelta, timezone

import jdatetime
from tortoise.timezone import now


def today_range() -> tuple[datetime, datetime]:
    start = now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


def get_current_timestamp() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def add_days_to_timestamp(timestamp: int, days: int) -> int:
    new_datetime = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc) + timedelta(days=days)
    return int(new_datetime.timestamp() * 1000)


def days_to_timestamp(days: int) -> int:
    return add_days_to_timestamp(get_current_timestamp(), days)


def to_jalali(dt: datetime) -> str:
    jalali = jdatetime.datetime.fromgregorian(datetime=dt)
    return jalali.strftime("%Y/%m/%d %H:%M")


def timestamp_to_days(timestamp: int) -> int:
    now = datetime.now(timezone.utc)
    target = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)

    return max(0, (target - now).days)