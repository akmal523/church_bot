"""
Handler for the "Basics of Orthodoxy" section.
Reads chapter list and content from locales/basics.json.
"""

import json
import os

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from locales.i18n import t

router = Router()

_BASICS_PATH = os.path.join("locales", "basics.json")


def _load_basics() -> dict:
    with open(_BASICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.callback_query(F.data == "basics:menu")
async def cb_basics_menu(callback: CallbackQuery, lang: str) -> None:
    data = _load_basics()
    buttons = [
        [InlineKeyboardButton(text=ch["title"][lang], callback_data=f"basics_view:{ch['id']}")]
        for ch in data["chapters"]
    ]
    buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")])

    await callback.message.edit_text(
        data["menu_title"][lang],
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("basics_view:"))
async def cb_basics_view(callback: CallbackQuery, lang: str) -> None:
    ch_id = callback.data.split(":")[1]
    data = _load_basics()
    chapter = next((c for c in data["chapters"] if c["id"] == ch_id), None)

    if not chapter:
        await callback.answer("Not found", show_alert=True)
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="basics:menu")]
    ])
    await callback.message.edit_text(chapter["content"][lang], reply_markup=kb)
    await callback.answer()
