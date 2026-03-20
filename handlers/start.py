"""
/start handler, language selection, and main menu navigation.
"""

from contextlib import suppress

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from database.crud import get_or_create_user, set_user_language
from keyboards.kb import (
    back_to_menu_keyboard,
    lang_keyboard,
    main_menu_keyboard,
    remove_kb,
)
from locales.i18n import t

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await get_or_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
    )
    await message.answer(
        t("welcome", lang="ru"),
        reply_markup=lang_keyboard(),
    )


@router.callback_query(F.data == "lang:selection")
async def cb_change_lang_menu(callback: CallbackQuery, lang: str) -> None:
    """Opens the language selection menu from the main menu."""
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            t("welcome", lang),
            reply_markup=lang_keyboard(),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("lang:"))
async def cb_set_lang(callback: CallbackQuery) -> None:
    """Sets the selected language in the database."""
    new_lang = callback.data.split(":")[1]
    if new_lang == "selection":
        return

    await set_user_language(callback.from_user.id, new_lang)

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            t("language_set", new_lang),
            reply_markup=main_menu_keyboard(new_lang),
        )
    await callback.answer()


@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery, lang: str) -> None:
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            t("main_menu", lang=lang),
            reply_markup=main_menu_keyboard(lang),
        )
    await callback.answer()


@router.callback_query(F.data == "about")
async def cb_about(callback: CallbackQuery, lang: str) -> None:
    await callback.message.edit_text(
        t("about", lang=lang),
        reply_markup=back_to_menu_keyboard(lang),
        disable_web_page_preview=True,
    )
    await callback.answer()


@router.message(F.text.in_(["Назад", "Back", "Orqaga", "Орқага"]))
async def handle_reply_back_btn(message: Message, lang: str) -> None:
    """Handles reply keyboard back buttons by switching to inline main menu."""
    msg = await message.answer("🔄", reply_markup=remove_kb())
    await msg.delete()
    await message.answer(
        t("main_menu", lang=lang),
        reply_markup=main_menu_keyboard(lang),
    )
