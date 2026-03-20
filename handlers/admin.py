"""
Admin panel — questions management and notifications toggle.
"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import settings
from database.crud import (
    answer_question,
    get_or_create_user,
    get_unanswered_questions,
    set_user_notifications,
)
from keyboards.kb import (
    admin_menu_keyboard,
    admin_question_keyboard,
    back_to_menu_keyboard,
)
from locales.i18n import t

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

@router.message(Command("admin"))
async def cmd_admin(message: Message, lang: str) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(t("not_authorized", lang=lang))
        return
    await message.answer(t("admin_menu", lang=lang), reply_markup=admin_menu_keyboard(lang))


@router.callback_query(F.data == "admin:menu")
async def cb_admin_menu(callback: CallbackQuery, lang: str) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t("not_authorized", lang=lang), show_alert=True)
        return
    await callback.message.edit_text(
        t("admin_menu", lang=lang),
        reply_markup=admin_menu_keyboard(lang),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# Questions management
# ---------------------------------------------------------------------------

class AnswerState(StatesGroup):
    waiting_for_answer = State()


@router.callback_query(F.data == "admin:questions")
async def cb_admin_questions(callback: CallbackQuery, lang: str) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t("not_authorized", lang=lang), show_alert=True)
        return

    questions = await get_unanswered_questions()
    if not questions:
        await callback.message.edit_text(
            t("admin_no_questions", lang=lang),
            reply_markup=admin_menu_keyboard(lang),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        t("admin_menu", lang=lang),
        reply_markup=admin_menu_keyboard(lang),
    )

    for q in questions[:10]:
        user_name = q.user.full_name if q.user else str(q.user_id)
        date_str = q.created_at.strftime("%d.%m.%Y")
        text = t("admin_question_item", lang=lang, id=q.id, user=user_name, date=date_str, text=q.text)
        await callback.message.answer(text, reply_markup=admin_question_keyboard(q.id, lang))

    await callback.answer()


@router.callback_query(F.data.startswith("admin:answer:"))
async def cb_start_answer(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t("not_authorized", lang=lang), show_alert=True)
        return

    question_id = int(callback.data.split(":")[2])
    await state.set_state(AnswerState.waiting_for_answer)
    await state.update_data(question_id=question_id, lang=lang)

    cancel_kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="admin:cancel_answer")
    ]])
    await callback.message.answer(
        t("admin_answer_prompt", lang=lang, id=question_id),
        reply_markup=cancel_kb,
    )
    await callback.answer()


@router.callback_query(F.data == "admin:cancel_answer")
async def cb_cancel_answer(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.clear()
    await callback.message.edit_text(
        t("action_cancelled", lang=lang),
        reply_markup=admin_menu_keyboard(lang),
    )
    await callback.answer()


@router.message(AnswerState.waiting_for_answer)
async def handle_answer_text(message: Message, state: FSMContext, lang: str) -> None:
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    question_id = data["question_id"]
    answered_lang = data.get("lang", lang)

    q = await answer_question(
        question_id=question_id,
        answer_text=message.text,
        answered_by=message.from_user.id,
    )
    await state.clear()

    if q is None:
        await message.answer("Question not found.")
        return

    # Notify the original user in their language
    user_lang = q.user.language if q.user else "ru"
    try:
        await message.bot.send_message(
            q.user_id,
            t("answer_received", lang=user_lang, answer=message.text),
        )
    except Exception:
        pass

    await message.answer(
        t("admin_answer_sent", lang=answered_lang),
        reply_markup=admin_menu_keyboard(answered_lang),
    )


# ---------------------------------------------------------------------------
# Notifications toggle (accessible by all users)
# ---------------------------------------------------------------------------

@router.callback_query(F.data == "notif:toggle")
async def cb_notif_toggle(callback: CallbackQuery, lang: str) -> None:
    user = await get_or_create_user(
        callback.from_user.id,
        callback.from_user.username,
        callback.from_user.full_name,
    )
    new_state = not user.notifications_enabled
    await set_user_notifications(callback.from_user.id, new_state)

    key = "notifications_on" if new_state else "notifications_off"
    await callback.message.edit_text(
        t(key, lang=lang),
        reply_markup=back_to_menu_keyboard(lang),
    )
    await callback.answer()
