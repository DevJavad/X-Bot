from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder as Builder

from app.settings import Config
from app.enums import UserRole
from .data import CoreAction as Action, CoreCB as CB, BackAction, BackCB


def start_button(role: UserRole) -> Markup:
    builder = Builder()

    builder.button(
        text=_("button:purchase"),
        # icon_custom_emoji_id=Emoji.PURCHASE,
        style=ButtonStyle.PRIMARY,
        callback_data=CB(action=Action.PURCHASE),
    )

    # builder.button(
    #     text=_("button:renewal"),
    #     # icon_custom_emoji_id=Emoji.RENEWAL,
    #     style=ButtonStyle.PRIMARY,
    #     callback_data=CB(action=Action.RENEWAL),
    # )

    builder.button(
        text=_("button:deposit"),
        # icon_custom_emoji_id=Emoji.DEPOSIT,
        style=ButtonStyle.PRIMARY,
        callback_data=CB(action=Action.DEPOSIT),
    )

    builder.button(
        text=_("button:profile"),
        # icon_custom_emoji_id=Emoji.PROFILE,
        style=ButtonStyle.PRIMARY,
        callback_data=CB(action=Action.PROFILE),
    )

    builder.button(
        text=_("button:services"),
        # icon_custom_emoji_id=Emoji.SERVICES,
        style=ButtonStyle.PRIMARY,
        callback_data=CB(action=Action.SERVICES),
    )

    builder.button(
        text=_("button:invoices"),
        # icon_custom_emoji_id=Emoji.INVOICES,
        style=ButtonStyle.PRIMARY,
        callback_data=CB(action=Action.INVOICES),
    )

    builder.button(
        text=_("button:trial"),
        # icon_custom_emoji_id=Emoji.TRIAL,
        style=ButtonStyle.PRIMARY,
        callback_data=CB(action=Action.TRIAL),
    )

    builder.button(
        text=_("button:invite"),
        # icon_custom_emoji_id=Emoji.INVITE,
        style=ButtonStyle.PRIMARY,
        callback_data=CB(action=Action.INVITE),
    )

    builder.button(
        text=_("button:support"),
        # icon_custom_emoji_id=Emoji.SUPPORT,
        style=ButtonStyle.PRIMARY,
        url="https://t.me/PyJavad/XonlineVPNSupport",
    )

    # builder.button(
    #     text=_("button:tutorial"),
    #     # icon_custom_emoji_id=Emoji.TUTORIAL,
    #     style=ButtonStyle.PRIMARY,
    #     callback_data=CB(action=Action.TUTORIAL),
    # )

    layout = [2, 2, 2, 2]

    if role in (UserRole.ADMIN, UserRole.OWNER):
        builder.button(
            text=_("button:management"),
            # icon_custom_emoji_id=Emoji.MANAGEMENT,
            style=ButtonStyle.SUCCESS,
            callback_data=CB(action=Action.MANAGEMENT),
        )
        layout.append(1)

    builder.adjust(*layout)
    return builder.as_markup()


def join_button(config: Config) -> Markup:
    builder = Builder()

    builder.button(
        text=_("button:join"),
        style=ButtonStyle.PRIMARY,
        # icon_custom_emoji_id=Emoji.JOIN,
        url=f"https://t.me/{config.bot.channel_username}",
    )

    builder.button(
        text=_("button:joined"),
        style=ButtonStyle.SUCCESS,
        # icon_custom_emoji_id=Emoji.JOINED,
        callback_data=Action.JOINED,
    )

    builder.adjust(1, 1)
    return builder.as_markup()


def back_button(action: BackAction) -> Markup:
    builder = Builder()

    builder.button(
        text=_("button:back"),
        style=ButtonStyle.DANGER,
        # icon_custom_emoji_id=Emoji.BACK,
        callback_data=BackCB(action=action),
    )

    return builder.as_markup()