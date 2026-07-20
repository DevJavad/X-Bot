from math import ceil

from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.utils.keyboard import InlineKeyboardBuilder as Builder
from aiogram.utils.i18n import gettext as _

from app.bot.routers.core import BackCB, BackAction
from app.database.models import Service

from .data import ServiceAction, ServiceCB


SERVICES_PER_PAGE = 10


def services_button(services: list[Service], page: int = 1) -> Markup:
    builder = Builder()

    start = (page - 1) * SERVICES_PER_PAGE
    end = start + SERVICES_PER_PAGE

    for service in services[start:end]:
        builder.button(
            text=f"{service.name}",
            style=ButtonStyle.PRIMARY,
            callback_data=ServiceCB(action=ServiceAction.DETAILS, service_id=service.id),
        )

    total_pages = ceil(len(services) / SERVICES_PER_PAGE) if services else 1

    if page > 1:
        builder.button(
            text=_("button:previous"),
            style=ButtonStyle.SUCCESS,
            callback_data=ServiceCB(action=ServiceAction.PREVIOUS, page=page - 1),
        )

    if page < total_pages:
        builder.button(
            text=_("button:next"),
            style=ButtonStyle.SUCCESS,
            callback_data=ServiceCB(action=ServiceAction.NEXT, page=page + 1),
        )

    builder.button(
        text=_("button:back"),
        style=ButtonStyle.DANGER,
        callback_data=BackCB(action=BackAction.MAIN),
    )

    builder.adjust(1, 1, 1)
    return builder.as_markup()


def service_details_button(page: int) -> Markup:
    builder = Builder()

    builder.button(
        text=_("button:back"),
        style=ButtonStyle.DANGER,
        callback_data=ServiceCB(action=ServiceAction.PAGE, page=page),
    )

    return builder.as_markup()