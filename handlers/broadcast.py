"""
Broadcast handler — admin-only mass messaging with preview and confirmation.
"""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import settings
from database.crud import (
    create_broadcast,
    get_all_users_for_broadcast,
    mark_broadcast_sent,
)
from keyboards.kb import admin_menu_keyboard, confirm_broadcast_keyboard
from locales.i18n import t
from utils.broadcaster import broadcast_to_users

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


class BroadcastState(StatesGroup):
    waiting_for_text = State()
    confirming = State()


@router.callback_query(F.data == "admin:broadcast")
async def cb_broadcast_start(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t("not_authorized", lang=lang), show_alert=True)
        return

    cancel_kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="admin:broadcast_cancel")
    ]])
    await callback.message.edit_text(t("admin_broadcast_prompt", lang=lang), reply_markup=cancel_kb)
    await state.set_state(BroadcastState.waiting_for_text)
    await state.update_data(lang=lang)
    await callback.answer()


@router.message(BroadcastState.waiting_for_text)
async def handle_broadcast_text(message: Message, state: FSMContext, lang: str) -> None:
    if not is_admin(message.from_user.id):
        return

    if not message.text or not message.text.strip():
        await message.answer(t("admin_broadcast_prompt", lang=lang))
        return

    users = await get_all_users_for_broadcast()
    count = len(users)
    await state.update_data(broadcast_text=message.text.strip(), user_count=count)
    await message.answer(
        t("admin_broadcast_confirm", lang=lang, count=count, text=message.text.strip()),
        reply_markup=confirm_broadcast_keyboard(lang),
    )
    await state.set_state(BroadcastState.confirming)


@router.callback_query(F.data == "admin:broadcast_confirm")
async def cb_broadcast_confirm(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t("not_authorized", lang=lang), show_alert=True)
        return

    data = await state.get_data()
    text = data.get("broadcast_text", "")
    if not text:
        await callback.answer("No text", show_alert=True)
        return

    b = await create_broadcast(text=text, created_by=callback.from_user.id)
    users = await get_all_users_for_broadcast()
    user_ids = [u.id for u in users]

    await callback.message.edit_text("⏳ Sending... / Отправляем...")
    await state.clear()

    sent = await broadcast_to_users(callback.bot, user_ids, text)
    await mark_broadcast_sent(b.id, sent)

    await callback.message.answer(
        t("admin_broadcast_done", lang=lang, count=sent),
        reply_markup=admin_menu_keyboard(lang),
    )


@router.callback_query(F.data == "admin:broadcast_cancel")
async def cb_broadcast_cancel(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.clear()
    await callback.message.edit_text(
        t("action_cancelled", lang=lang),
        reply_markup=admin_menu_keyboard(lang),
    )
    await callback.answer()
