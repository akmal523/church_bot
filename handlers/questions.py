"""
User → diocese question handler with 24-hour rate limiting.
"""

from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import settings
from database.crud import create_question, get_last_question_time
from keyboards.kb import back_to_menu_keyboard, main_menu_keyboard
from locales.i18n import t

router = Router()


class QuestionStates(StatesGroup):
    waiting_for_text = State()


@router.callback_query(F.data == "ask:start")
async def ask_start(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    # Check cooldown before entering FSM state
    last_time = await get_last_question_time(callback.from_user.id)
    if last_time:
        elapsed = datetime.utcnow() - last_time
        cooldown = timedelta(hours=settings.QUESTION_COOLDOWN_HOURS)
        if elapsed < cooldown:
            remaining_hours = int((cooldown - elapsed).total_seconds() // 3600) + 1
            await callback.answer(
                t("question_cooldown", lang, hours=remaining_hours),
                show_alert=True,
            )
            return

    await callback.message.edit_text(
        t("ask_question_prompt", lang),
        reply_markup=back_to_menu_keyboard(lang),
    )
    await state.set_state(QuestionStates.waiting_for_text)
    await callback.answer()


@router.message(QuestionStates.waiting_for_text)
async def process_question(message: Message, state: FSMContext, lang: str) -> None:
    # Abort on commands
    if message.text and message.text.startswith("/"):
        await state.clear()
        return

    if not message.text or not message.text.strip():
        await message.answer(t("ask_question_prompt", lang), reply_markup=back_to_menu_keyboard(lang))
        return

    # Persist to DB
    await create_question(message.from_user.id, message.text.strip())

    # Forward to all admins
    username = f"@{message.from_user.username}" if message.from_user.username else "—"
    for admin_id in settings.ADMIN_IDS:
        try:
            await message.bot.send_message(
                admin_id,
                f"<b>📩 Новое обращение!</b>\n"
                f"От: {message.from_user.full_name} ({username})\n"
                f"ID: <code>{message.from_user.id}</code>\n\n"
                f"Текст: {message.text.strip()}",
            )
        except Exception:
            pass

    await message.answer(t("question_sent", lang), reply_markup=main_menu_keyboard(lang))
    await state.clear()
