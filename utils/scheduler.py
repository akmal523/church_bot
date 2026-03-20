"""
Daily notification scheduler.
Sends morning calendar briefings to users with notifications enabled.

Started as a background task from main.py:
    asyncio.create_task(run_daily_scheduler(bot))
"""

import asyncio
import logging
from datetime import date, datetime

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from database.crud import get_users_with_notifications
from locales.i18n import t, weekday_name
from utils.broadcaster import MAX_PER_SECOND
from utils.calendar_api import fetch_calendar_day

logger = logging.getLogger(__name__)

SEND_HOUR = 7
SEND_MINUTE = 0


async def send_daily_notification(bot: Bot, user_id: int, lang: str) -> None:
    today = date.today()
    data = await fetch_calendar_day(today, lang=lang)
    date_fmt = "%d.%m.%Y" if lang in ("ru", "uz", "uzl") else "%B %d, %Y"

    text = t(
        "calendar_today",
        lang=lang,
        date=today.strftime(date_fmt),
        weekday=weekday_name(today.weekday(), lang),
        tone_line="",
        feast=data.get("feast", "—"),
        readings=data.get("readings", "—"),
        fast=data.get("fast", "—"),
        saints=data.get("saints", "—"),
    )
    try:
        await bot.send_message(user_id, text)
    except TelegramForbiddenError:
        logger.debug("User %s blocked the bot — skipping notification", user_id)
    except Exception as exc:
        logger.debug("Could not send notification to %s: %s", user_id, exc)


async def run_daily_scheduler(bot: Bot) -> None:
    """Infinite loop that fires once per day at SEND_HOUR:SEND_MINUTE."""
    logger.info("Daily scheduler started")
    while True:
        now = datetime.now()
        next_run = now.replace(hour=SEND_HOUR, minute=SEND_MINUTE, second=0, microsecond=0)
        if next_run <= now:
            # Already past today's send time — schedule for tomorrow
            from datetime import timedelta
            next_run += timedelta(days=1)

        wait_seconds = (next_run - now).total_seconds()
        logger.info("Next daily notification in %.0f seconds", wait_seconds)
        await asyncio.sleep(wait_seconds)

        users = await get_users_with_notifications()
        logger.info("Sending daily notifications to %d users", len(users))
        delay = 1.0 / MAX_PER_SECOND
        for user in users:
            await send_daily_notification(bot, user.id, user.language)
            await asyncio.sleep(delay)
