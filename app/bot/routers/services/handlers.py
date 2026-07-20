import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from aioxui import XUI
from aioxui.enums import Calendar
from aioxui.utils import DateTime, Storage

from app.settings import Config
from app.bot.routers.core import CoreAction, CoreCB
from app.database.models import Service, User
from app.enums import ServiceStatus
from app.utils.constants import UNLIMITED, SERVICE_STATUS_MAP


from .data import ServiceAction, ServiceCB
from .buttons import services_button, service_details_button

router = Router(name=__name__)
logger = logging.getLogger(__name__)


def progress_bar(percent: float, length: int = 10) -> str:
    filled = round(percent / 100 * length)
    return "🟩" * filled + "⬜" * (length - filled)


@router.callback_query(CoreCB.filter(F.action == CoreAction.SERVICES))
async def services(query: CallbackQuery, user: User):
    services = await Service.filter(user=user)
    if not services:
        return await query.answer(_("notification:services:empty"), True)

    return await query.message.edit_text(
        _("message:services").format(count=len(services)),
        reply_markup=services_button(services),
    )


@router.callback_query(ServiceCB.filter(F.action == ServiceAction.DETAILS))
async def detail(
    query: CallbackQuery,
    user: User,
    xui: XUI,
    callback_data: ServiceCB,
    config: Config,
):
    service = await Service.get_or_none(id=callback_data.service_id, user=user)

    if service is None:
        return await query.answer(_("notification:service:not_found"), True)

    name = service.name
    sub_id = service.sub_id
    sub_url = config.xui.subscription_url(sub_id)

    traffic = await xui.client.get_traffic(name)

    if (
        service.expire_time
        and service.expire_time <= DateTime.now()
        and service.status == ServiceStatus.ACTIVE
    ):
        service.status = ServiceStatus.EXPIRED
        await service.save(update_fields=["status"])

    total_used = traffic.download + traffic.upload
    service.traffic_used = total_used
    await service.save(update_fields=["traffic_used"])

    traffic_limit = Storage.format(traffic.total) if traffic.total else UNLIMITED
    traffic_used = Storage.format(total_used)
    traffic_remaining = (
        Storage.format(max(traffic.total - total_used, 0))
        if traffic.total
        else UNLIMITED
    )

    if traffic.total:
        used_percent = min((total_used / traffic.total) * 100, 100)
        remaining_percent = max(100 - used_percent, 0)
    else:
        used_percent = None
        remaining_percent = None

    used_percent = (
        f"{used_percent:.1f}".rstrip("0").rstrip(".")
        if used_percent is not None
        else UNLIMITED
    )
    remaining_percent = (
        f"{remaining_percent:.1f}".rstrip("0").rstrip(".")
        if remaining_percent is not None
        else UNLIMITED
    )

    created_at = DateTime.to_calendar(
        int(service.created_at.timestamp() * 1000),
        Calendar.JALALI,
        "%Y/%m/%d - %H:%M",
    )

    if service.expire_time:
        expire_date = DateTime.to_calendar(
            service.expire_time, Calendar.JALALI, "%Y/%m/%d - %H:%M"
        )

        expiry_text = expire_date
    else:
        expiry_text = UNLIMITED

    last_online = DateTime.to_calendar(traffic.last_online, Calendar.JALALI, "%Y/%m/%d - %H:%M")

    text = _("message:service:details").format(
        name=name,
        status=SERVICE_STATUS_MAP.get(service.status, service.status),
        traffic_used=traffic_used,
        traffic_limit=traffic_limit,
        traffic_remaining=traffic_remaining,
        used_percent=used_percent,
        remaining_percent=remaining_percent,
        user_limit=service.user_limit or UNLIMITED,
        created_at=created_at,
        expire=expiry_text,
        last_online=last_online,
        sub_url=sub_url,
    )

    return await query.message.edit_text(
        text,
        reply_markup=service_details_button(callback_data.page or 1),
    )


@router.callback_query(ServiceCB.filter(F.action == ServiceAction.PAGE))
async def services_page(query: CallbackQuery, callback_data: ServiceCB, user: User):
    services = await Service.filter(user=user)

    await query.message.edit_text(
        _("message:services").format(count=len(services)),
        reply_markup=services_button(services, page=callback_data.page or 1),
    )