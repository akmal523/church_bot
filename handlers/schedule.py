"""
Service schedule handlers — weekly and daily view for a church.
"""

from datetime import date, timedelta

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.crud import get_church, get_schedule, get_schedules_for_church_week
from database.db import Schedule
from keyboards.kb import back_to_menu_keyboard, schedule_period_keyboard
from locales.i18n import t, weekday_name

router = Router()

WEEKDAY_NAMES_RU = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
WEEKDAY_NAMES_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _build_schedule_text(
    church_name: str,
    schedules: list[Schedule],
    start: date,
    lang: str,
) -> str:
    end = start + timedelta(days=6)
    fmt = "%d.%m" if lang == "ru" else "%m/%d"
    lines = [
        t("schedule_header", lang=lang, church=church_name,
          start=start.strftime(fmt), end=end.strftime(fmt))
    ]

    for i in range(7):
        day = start + timedelta(days=i)
        wd = day.weekday()

        day_entries = [
            s for s in schedules
            if (s.repeat_weekly and s.weekday == wd) or (s.specific_date == day)
        ]
        day_entries.sort(key=lambda s: s.service_time)

        lines.append(t(
            "schedule_day_header", lang=lang,
            weekday=weekday_name(wd, lang),
            date=day.strftime("%d.%m.%Y"),
        ))

        if not day_entries:
            lines.append(t("schedule_no_services", lang=lang))
        else:
            for entry in day_entries:
                svc = entry.service_name_ru if lang == "ru" else entry.service_name_en
                notes = entry.notes_ru if lang == "ru" else entry.notes_en
                notes_str = t("schedule_notes", lang=lang, notes=notes) if notes else ""
                lines.append(t(
                    "schedule_entry", lang=lang,
                    time=entry.service_time.strftime("%H:%M"),
                    service=svc,
                    notes=notes_str,
                ))

    return "\n".join(lines)


@router.callback_query(F.data.startswith("schedule:church:"))
async def cb_schedule_menu(callback: CallbackQuery, lang: str) -> None:
    """Show period selector (today / week) for a church's schedule."""
    church_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        t("choose_schedule_period", lang=lang),
        reply_markup=schedule_period_keyboard(church_id, lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("sch:"))
async def cb_show_schedule(callback: CallbackQuery, lang: str) -> None:
    """Show today's or this week's schedule for a church (ServiceSchedule table)."""
    parts = callback.data.split(":")
    period = parts[1]
    church_id = int(parts[2])

    church = await get_church(church_id)
    if not church:
        await callback.answer("Not found", show_alert=True)
        return

    schedules = await get_schedule(church_id, period)

    if not schedules:
        text = t("no_schedule", lang=lang)
    else:
        period_key = "schedule_header_today" if period == "today" else "schedule_header_week"
        lines = [t(period_key, lang=lang)]
        for s in schedules:
            title = getattr(s, f"title_{lang}", None) or s.title_ru
            lines.append(f"{s.date.strftime('%d.%m.%Y')} {s.time} — {title}")
        text = "\n".join(lines)

    await callback.message.edit_text(
        text,
        reply_markup=schedule_period_keyboard(church_id, lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("schedule:"))
async def cb_schedule_weekly(callback: CallbackQuery, lang: str) -> None:
    """Show the full weekly schedule for a church (Schedule table, repeat_weekly logic)."""
    church_id = int(callback.data.split(":")[1])
    church = await get_church(church_id)
    if not church:
        await callback.answer("Not found", show_alert=True)
        return

    today = date.today()
    start = today - timedelta(days=today.weekday())  # Monday
    schedules = await get_schedules_for_church_week(church_id, start)

    church_name = church.name_ru if lang == "ru" else (church.name_en or church.name_ru)
    text = _build_schedule_text(church_name, schedules, start, lang)

    back_kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t("btn_back", lang), callback_data=f"church:{church_id}")
    ]])
    await callback.message.edit_text(text, reply_markup=back_kb)
    await callback.answer()
