"""
Handlers for church search: nearest by geolocation and browse by city.
"""

from contextlib import suppress

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message

from database.crud import get_all_cities, get_church, get_churches_by_city, get_churches_near
from keyboards.kb import (
    back_to_menu_keyboard,
    church_detail_keyboard,
    churches_keyboard,
    cities_keyboard,
    location_request_keyboard,
    main_menu_keyboard,
    nearest_churches_keyboard,
    remove_kb,
)
from locales.i18n import t

router = Router()


@router.callback_query(F.data == "geo:start")
async def cb_geo_start(callback: CallbackQuery, lang: str) -> None:
    await callback.message.answer(
        t("send_location_prompt", lang=lang),
        reply_markup=location_request_keyboard(lang),
    )
    await callback.answer()


@router.message(F.location)
async def handle_location(message: Message, lang: str) -> None:
    lat = message.location.latitude
    lon = message.location.longitude

    churches_dist = await get_churches_near(lat, lon, limit=5)
    if not churches_dist:
        await message.answer(
            t("no_churches_found", lang=lang),
            reply_markup=back_to_menu_keyboard(lang),
        )
        return

    await message.answer(
        t("nearest_churches_result", lang=lang),
        reply_markup=nearest_churches_keyboard(churches_dist, lang),
    )


@router.message(F.text.in_([t("btn_back", l) for l in ["ru", "en", "uz", "uzl"]]))
async def handle_location_back(message: Message, lang: str) -> None:
    """Dismiss location reply keyboard and return to main menu."""
    remove_msg = await message.answer("🔄", reply_markup=remove_kb())
    await remove_msg.delete()
    await message.answer(
        t("main_menu", lang=lang),
        reply_markup=main_menu_keyboard(lang),
    )


@router.callback_query(F.data == "cities:list")
async def cb_cities_list(callback: CallbackQuery, lang: str) -> None:
    cities = await get_all_cities()
    if not cities:
        await callback.answer(t("no_churches_found", lang=lang), show_alert=True)
        return
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            t("choose_city", lang=lang),
            reply_markup=cities_keyboard(cities, lang),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("city:"))
async def cb_city_churches(callback: CallbackQuery, lang: str) -> None:
    city_id = int(callback.data.split(":")[1])
    churches = await get_churches_by_city(city_id)
    if not churches:
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                t("no_churches_found", lang=lang),
                reply_markup=back_to_menu_keyboard(lang),
            )
        await callback.answer()
        return

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            t("choose_church", lang=lang),
            reply_markup=churches_keyboard(churches, lang, back_cb="cities:list"),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("church:"))
async def cb_church_detail(callback: CallbackQuery, lang: str) -> None:
    church_id = int(callback.data.split(":")[1])
    church = await get_church(church_id)
    if not church:
        await callback.answer("Not found", show_alert=True)
        return

    name = getattr(church, f"name_{lang}", None) or church.name_ru
    address = getattr(church, f"address_{lang}", None) or church.address_ru
    description = getattr(church, f"description_{lang}", None) or church.description_ru or ""
    phone_line = t("church_phone", lang, phone=church.phone) if church.phone else ""

    text = t(
        "church_detail",
        lang=lang,
        name=name,
        address=address,
        phone_line=phone_line,
        description=description,
    )

    kb = church_detail_keyboard(
        church_id=church.id,
        lang=lang,
        city_id=church.city_id,
        google_url=church.google_maps_url,
        yandex_url=church.yandex_maps_url,
    )

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
