"""
Admin schedule management — manual entry and CSV bulk upload.
"""

import csv
import io
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import settings
from database.crud import add_schedule_record
from keyboards.kb import admin_menu_keyboard, admin_schedule_keyboard
from locales.i18n import t

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


class AdminScheduleManual(StatesGroup):
    church_id = State()
    date = State()
    time = State()
    titles = State()


class AdminScheduleFile(StatesGroup):
    waiting_for_file = State()


@router.callback_query(F.data == "admin:schedule")
async def admin_sch_menu(callback: CallbackQuery, lang: str) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t("not_authorized", lang=lang), show_alert=True)
        return
    await callback.message.edit_text(
        t("admin_sch_choose_method", lang=lang),
        reply_markup=admin_schedule_keyboard(lang),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# Manual entry
# ---------------------------------------------------------------------------

@router.callback_query(F.data == "admin:sch:manual")
async def manual_start(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t("not_authorized", lang=lang), show_alert=True)
        return
    await callback.message.answer(t("admin_sch_enter_church_id", lang=lang))
    await state.set_state(AdminScheduleManual.church_id)
    await callback.answer()


@router.message(AdminScheduleManual.church_id)
async def manual_church(message: Message, state: FSMContext, lang: str) -> None:
    if not message.text or not message.text.strip().isdigit():
        await message.answer(t("admin_sch_invalid_id", lang=lang))
        return
    await state.update_data(church_id=int(message.text.strip()))
    await message.answer(t("admin_sch_enter_date", lang=lang))
    await state.set_state(AdminScheduleManual.date)


@router.message(AdminScheduleManual.date)
async def manual_date(message: Message, state: FSMContext, lang: str) -> None:
    try:
        parsed = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        await message.answer(t("admin_sch_invalid_date", lang=lang))
        return
    await state.update_data(date=parsed)
    await message.answer(t("admin_sch_enter_time", lang=lang))
    await state.set_state(AdminScheduleManual.time)


@router.message(AdminScheduleManual.time)
async def manual_time(message: Message, state: FSMContext, lang: str) -> None:
    try:
        parts = message.text.strip().split(":")
        assert len(parts) == 2
        int(parts[0]), int(parts[1])
    except (AssertionError, ValueError, AttributeError):
        await message.answer(t("admin_sch_invalid_time", lang=lang))
        return
    await state.update_data(time=message.text.strip())
    await message.answer(t("admin_sch_enter_titles", lang=lang))
    await state.set_state(AdminScheduleManual.titles)


@router.message(AdminScheduleManual.titles)
async def manual_titles(message: Message, state: FSMContext, lang: str) -> None:
    parts = message.text.split("|")
    data = await state.get_data()
    data.update({
        "title_ru": parts[0].strip() if len(parts) > 0 else "",
        "title_en": parts[1].strip() if len(parts) > 1 else "",
        "title_uz": parts[2].strip() if len(parts) > 2 else "",
        "title_uzl": parts[3].strip() if len(parts) > 3 else "",
    })
    await add_schedule_record(data)
    await state.clear()
    await message.answer(
        t("admin_sch_record_added", lang=lang),
        reply_markup=admin_menu_keyboard(lang),
    )


# ---------------------------------------------------------------------------
# CSV bulk upload
# ---------------------------------------------------------------------------

@router.callback_query(F.data == "admin:sch:file")
async def file_start(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t("not_authorized", lang=lang), show_alert=True)
        return
    await callback.message.answer(t("admin_sch_upload_csv_prompt", lang=lang))
    await state.set_state(AdminScheduleFile.waiting_for_file)
    await callback.answer()


@router.message(AdminScheduleFile.waiting_for_file, F.document)
async def process_file(message: Message, state: FSMContext, bot: Bot, lang: str) -> None:
    file_info = await bot.get_file(message.document.file_id)
    downloaded = await bot.download_file(file_info.file_path)
    text_data = downloaded.getvalue().decode("utf-8")

    reader = csv.DictReader(io.StringIO(text_data))
    count = 0
    errors = 0
    for row in reader:
        try:
            data = {
                "church_id": int(row["church_id"]),
                "date": datetime.strptime(row["date"], "%Y-%m-%d").date(),
                "time": row["time"],
                "title_ru": row.get("title_ru", ""),
                "title_en": row.get("title_en", ""),
                "title_uz": row.get("title_uz", ""),
                "title_uzl": row.get("title_uzl", ""),
            }
            await add_schedule_record(data)
            count += 1
        except (KeyError, ValueError):
            errors += 1

    await state.clear()
    await message.answer(
        t("admin_sch_csv_done", lang=lang, count=count, errors=errors),
        reply_markup=admin_menu_keyboard(lang),
    )
