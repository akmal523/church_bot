import json
import os
import asyncio
import logging
from datetime import date, timedelta

logger = logging.getLogger(__name__)

def cyrillic_to_latin(text: str) -> str:
    """Транслитерация узбекской кириллицы в латиницу."""
    mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'j', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'x', 'ц': 's', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh',
        'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'ў': "o'", 'қ': 'q', 'ғ': "g'", 'ҳ': 'h',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'J', 'З': 'Z',
        'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'X', 'Ц': 'S', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sh',
        'Ў': "O'", 'Қ': 'Q', 'Ғ': "G'", 'Ҳ': 'H'
    }
    res = ""
    for char in text:
        low = char.lower()
        if low in mapping:
            res += mapping[low].upper() if char.isupper() else mapping[low]
        else:
            res += char
    return res

def get_offline_fast(target_date: date, lang: str) -> str:
    """Локальный расчет постных дней (Среда и Пятница)."""
    is_fast = target_date.weekday() in [2, 4] # Wednesday, Friday
    
    fast_map = {
        "ru": "Пост" if is_fast else "Поста нет",
        "en": "Fast" if is_fast else "No fast",
        "uz": "Рўза" if is_fast else "Рўза йўқ",
        "uzl": "Ro'za" if is_fast else "Ro'za yo'q"
    }
    return fast_map.get(lang, fast_map["ru"])

async def fetch_calendar_day(target_date: date, lang: str) -> dict:
    """Получение данных о святых из локального JSON и расчет поста."""
    path = os.path.join("locales", "saints.json")
    saints_data = {}
    
    # Пытаемся загрузить офлайн базу святых
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                saints_data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading saints.json: {e}")

    day_key = target_date.strftime("%m-%d")
    day_info = saints_data.get(day_key, {})
    
    # Приоритет: текущий язык -> русский -> заглушка
    feast = day_info.get(lang) or day_info.get("ru")
    
    if not feast:
        if lang == "ru": feast = "День памяти святых"
        elif lang == "en": feast = "Commemoration of Saints"
        elif lang == "uz": feast = "Муқаддаслар хотираси"
        elif lang == "uzl": feast = "Muqaddaslar xotirasi"
        else: feast = "—"
    
    # Если для узбекской латиницы нет перевода, транслитерируем русский
    if lang == "uzl" and not day_info.get("uzl"):
        feast = cyrillic_to_latin(day_info.get("ru", feast))

    return {
        "feast": feast,
        "fast": get_offline_fast(target_date, lang),
        "weekday": target_date.weekday(),
        "saints": "—", # Офлайн чтений и подробных житий нет
        "readings": "—"
    }

async def fetch_calendar_week(start_date: date, lang: str) -> list[dict]:
    """Генерация данных на неделю."""
    tasks = [fetch_calendar_day(start_date + timedelta(days=i), lang) for i in range(7)]
    return await asyncio.gather(*tasks)
