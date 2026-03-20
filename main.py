"""
Orthodox Church Bot — Uzbekistan
Православный бот — Узбекистан
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from database.db import init_db
from handlers import start, churches, schedule, calendar, admin, broadcast, questions, basics, admin_schedule
from utils.middleware import UserLanguageMiddleware
from utils.scheduler import run_daily_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.update.outer_middleware(UserLanguageMiddleware())

    dp.include_routers(
        start.router,
        basics.router,
        churches.router,
        schedule.router,
        calendar.router,
        questions.router,
        broadcast.router,
        admin_schedule.router,
        admin.router,
    )

    await init_db()
    logger.info("Bot started / Бот запущен")

    # Start daily notification scheduler as a background task
    asyncio.create_task(run_daily_scheduler(bot))

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
