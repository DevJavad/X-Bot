import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.utils.i18n import gettext as _
from aioxui import XUI
from aioxui.models import Client
from aioxui.utils import DateTime, Storage

from app.bot.routers.core import back_button, BackAction, CoreAction, CoreCB
from app.database.models import Service, User
from app.settings import Config
from app.utils.constants import TRIAL
from app.utils.functions import generate_qrcode

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.callback_query(CoreCB.filter(F.action == CoreAction.TRIAL))
async def trial(query: CallbackQuery, user: User, xui: XUI, config: Config):
    if user.trial_used:
        return await query.answer(_("notification:trial_used"), True)

    user_id = user.user_id
    name: str = f"test-{user_id}"

    try:
        traffic = Storage.from_unit(TRIAL.TRAFFIC, TRIAL.TRAFFIC_UNIT)
        expire_time = DateTime.after(**TRIAL.EXPIRY)

        client = Client(
            email=name,
            totalGB=traffic,
            expiryTime=expire_time,
            limitIp=TRIAL.IP_LIMTI,
            tgId=user_id,
            group=TRIAL.GROUP,
        )
        result = await xui.client.add(TRIAL.INBOUND_ID, client)

        await Service.create(
            user=user,
            uuid=result.uuid,
            name=result.email,
            sub_id=result.sub_id,
            traffic_limit=traffic,
            ip_limit=TRIAL.IP_LIMTI,
            expire_time=expire_time,
        )

        user.trial_used = True
        await user.save()

        sub_url = config.xui.subscription_url(result.sub_id)
        qrcode = generate_qrcode(sub_url)

        return await query.message.answer_photo(
            photo=BufferedInputFile(qrcode, filename=f"{result.sub_id}.png"),
            caption=_("message:trial").format(name=name, sub_url=sub_url),
        )

    except Exception as error:
        logger.error(error)