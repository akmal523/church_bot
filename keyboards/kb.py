"""
Keyboard builders — all inline and reply keyboards.
"""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from database.db import Church, City
from locales.i18n import t

def remove_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def admin_question_keyboard(question_id: int, lang: str) -> InlineKeyboardMarkup:
    """
    Кнопка 'Ответить' под вопросом в админ-панели.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("admin_btn_answer", lang, id=question_id),
            callback_data=f"admin:answer:{question_id}",
        )]
    ])

def confirm_broadcast_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Кнопки подтверждения или отмены рассылки.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("admin_btn_confirm", lang), callback_data="admin:broadcast_confirm"),
            InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="admin:broadcast_cancel"),
        ]
    ])

def schedule_period_keyboard(church_id: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_today", lang), callback_data=f"sch:today:{church_id}")],
        [InlineKeyboardButton(text=t("btn_week", lang), callback_data=f"sch:week:{church_id}")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data=f"church:{church_id}")]
    ])

def admin_schedule_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("admin_sch_manual", lang), callback_data="admin:sch:manual")],
        [InlineKeyboardButton(text=t("admin_sch_file", lang), callback_data="admin:sch:file")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="admin:menu")]
    ])



def basics_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Заглушка для меню 'Основы православия', чтобы не было ошибок при нажатии.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")]
    ])


def nearest_churches_keyboard(churches_with_dist: list, lang: str) -> InlineKeyboardMarkup:
    """
    """
    keyboard = []
    for church, dist in churches_with_dist:
        name = getattr(church, f"name_{lang}", church.name_ru)
        dist_text = t("distance_km", lang, dist=dist)
        btn_text = f"{name} ({dist_text})"
        keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=f"church:{church.id}")])
    
    keyboard.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
        ],
        [
            InlineKeyboardButton(text="🇺🇿 Ўзбек (Кирилл)", callback_data="lang:uz"),
            InlineKeyboardButton(text="🇺🇿 O'zbek (Lotin)", callback_data="lang:uzl"),
        ],
    ])

def location_request_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_share_location", lang), request_location=True)],
            [KeyboardButton(text=t("btn_back", lang))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Главное меню со всеми кнопками: Поиск, Город, Календарь, Вопросы, Основы, Язык.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_nearest_church", lang), callback_data="geo:start"),
            InlineKeyboardButton(text=t("btn_by_city", lang), callback_data="cities:list"),
        ],
        [
            InlineKeyboardButton(text=t("btn_calendar", lang), callback_data="cal:today"),
            InlineKeyboardButton(text=t("btn_ask_question", lang), callback_data="ask:start"),
        ],
        [
            InlineKeyboardButton(text=t("btn_basics", lang), callback_data="basics:menu"),
            InlineKeyboardButton(text=t("btn_language", lang), callback_data="lang:selection"),
        ]
    ])

def cities_keyboard(cities: list[City], lang: str) -> InlineKeyboardMarkup:
    keyboard = []
    # По 2 города в ряд
    for i in range(0, len(cities), 2):
        row = []
        c1 = cities[i]
        name1 = getattr(c1, f"name_{lang}", c1.name_ru)
        row.append(InlineKeyboardButton(text=name1, callback_data=f"city:{c1.id}"))
        
        if i + 1 < len(cities):
            c2 = cities[i+1]
            name2 = getattr(c2, f"name_{lang}", c2.name_ru)
            row.append(InlineKeyboardButton(text=name2, callback_data=f"city:{c2.id}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def churches_keyboard(churches: list[Church], lang: str, city_id: int = None, back_cb: str = "cities:list") -> InlineKeyboardMarkup:
    keyboard = []
    for ch in churches:
        name = getattr(ch, f"name_{lang}", ch.name_ru)
        keyboard.append([InlineKeyboardButton(text=name, callback_data=f"church:{ch.id}")])
    
    keyboard.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data=back_cb)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def church_detail_keyboard(church_id: int, lang: str, city_id: int, google_url: str = None, yandex_url: str = None) -> InlineKeyboardMarkup:
    keyboard = []
    # Кнопка расписания (полная информация)
    keyboard.append([InlineKeyboardButton(text=t("btn_schedule", lang), callback_data=f"schedule:church:{church_id}")])
    
    # Кнопки навигации, если есть ссылки
    nav_row = []
    if google_url:
        nav_row.append(InlineKeyboardButton(text=t("btn_navigate_google", lang), url=google_url))
    if yandex_url:
        nav_row.append(InlineKeyboardButton(text=t("btn_navigate_yandex", lang), url=yandex_url))
    if nav_row:
        keyboard.append(nav_row)
        
    keyboard.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data=f"city:{city_id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def admin_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("admin_btn_questions", lang), callback_data="admin:questions")],
        [InlineKeyboardButton(text=t("admin_btn_broadcast", lang), callback_data="admin:broadcast")],
        [InlineKeyboardButton(text=t("admin_btn_edit_schedule", lang), callback_data="admin:schedule")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")],
    ])

def back_to_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")]
    ])
