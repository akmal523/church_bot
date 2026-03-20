"""
Orthodox calendar handler — shows today's feast, fast level, and saints.
"""

import logging
from contextlib import suppress
from datetime import date

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from keyboards.kb import back_to_menu_keyboard
from locales.i18n import t, weekday_name
from utils.calendar_api import fetch_calendar_day

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "cal:today")
async def show_calendar(callback: CallbackQuery, lang: str) -> None:
    today = date.today()

    data = await fetch_calendar_day(today, lang=lang)

    text = t(
        "calendar_today",
        lang=lang,
        date=today.strftime("%d.%m.%Y"),
        weekday=weekday_name(today.weekday(), lang),
        tone_line="",
        feast=data.get("feast", "—"),
        readings=data.get("readings", "—"),
        fast=data.get("fast", "—"),
        saints=data.get("saints", "—"),
    )

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text,
            reply_markup=back_to_menu_keyboard(lang),
        )
    await callback.answer()
