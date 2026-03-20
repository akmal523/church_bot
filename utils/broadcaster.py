"""
Broadcast utility — sends messages to all users respecting Telegram limits.
Telegram allows ~30 messages/second; we use a conservative 25 msg/s.
"""

import asyncio
import logging
from typing import Callable

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

logger = logging.getLogger(__name__)

MAX_PER_SECOND = 25


async def broadcast_to_users(
    bot: Bot,
    user_ids: list[int],
    text: str,
    on_progress: Callable[[int, int], None] | None = None,
) -> int:
    """
    Send text to all user_ids. Returns number of successfully delivered messages.
    on_progress(sent, total) is called after each batch.
    """
    sent = 0
    total = len(user_ids)
    batch_delay = 1.0 / MAX_PER_SECOND

    for i, uid in enumerate(user_ids):
        try:
            await bot.send_message(uid, text)
            sent += 1
        except TelegramForbiddenError:
            # User blocked the bot
            logger.debug("User %s blocked the bot — skipping", uid)
        except TelegramRetryAfter as e:
            logger.warning("Flood control: sleeping %ss", e.retry_after)
            await asyncio.sleep(e.retry_after)
            try:
                await bot.send_message(uid, text)
                sent += 1
            except Exception:
                pass
        except Exception as exc:
            logger.error("Broadcast error for user %s: %s", uid, exc)

        await asyncio.sleep(batch_delay)

        if on_progress and (i + 1) % 50 == 0:
            on_progress(sent, total)

    return sent
