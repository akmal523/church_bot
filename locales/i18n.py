"""
Localization — Russian (ru), English (en),
Uzbek Cyrillic (uz), Uzbek Latin (uzl).

Usage:
    from locales.i18n import t
    text = t("welcome", lang="uz")
"""

from typing import Any

LANGS = ("ru", "en", "uz", "uzl")

_STRINGS: dict[str, dict[str, str]] = {
    "welcome": {
        "ru": "☩ <b>Добро пожаловать!</b>\n\nПравославный помощник для верующих в Узбекистане.\nРасписание служб, православный календарь, информация о приходах.\n\nВыберите язык:",
        "en": "☩ <b>Welcome!</b>\n\nOrthodox assistant for believers in Uzbekistan.\nService schedules, Orthodox calendar, parish information.\n\nChoose your language:",
        "uz": "☩ <b>Хуш келибсиз!</b>\n\nЎзбекистондаги православ мўминлар учун ёрдамчи.\nИбодат жадвали, православ тақвими, черков маълумотлари.\n\nТилни танланг:",
        "uzl": "☩ <b>Xush kelibsiz!</b>\n\nO'zbekistondagi pravoslav mo'minlar uchun yordamchi.\nIbodat jadvali, pravoslav taqvimi, cherkov ma'lumotlari.\n\nTilni tanlang:",
    },
    "language_set": {
        "ru": "Язык установлен: Русский 🇷🇺",
        "en": "Language set: English 🇬🇧",
        "uz": "Тил танланди: Ўзбекча (Кирилл) 🇺🇿",
        "uzl": "Til tanlandi: O'zbekcha (Lotin) 🇺🇿",
    },
    "main_menu": {
        "ru": "☩ Главное меню",
        "en": "☩ Main Menu",
        "uz": "☩ Асосий меню",
        "uzl": "☩ Asosiy menyu",
    },
    "btn_nearest_church": {
        "ru": "📍 Ближайший храм",
        "en": "📍 Nearest Church",
        "uz": "📍 Яқин черков",
        "uzl": "📍 Yaqin cherkov",
    },
    "btn_by_city": {
        "ru": "🏙 Выбрать город",
        "en": "🏙 Choose City",
        "uz": "🏙 Шаҳарни танлаш",
        "uzl": "🏙 Shaharni tanlash",
    },
    "btn_calendar": {
        "ru": "📅 Православный календарь",
        "en": "📅 Orthodox Calendar",
        "uz": "📅 Православ тақвими",
        "uzl": "📅 Pravoslav taqvimi",
    },
    "btn_ask_question": {
        "ru": "✉️ Служба поддержки",
        "en": "✉️ Support Service",
        "uz": "✉️ Қўллаб-қувватлаш хизмати",
        "uzl": "✉️ Qo'llab-quvvatlash xizmati",
    },
    "btn_notifications": {
        "ru": "🔔 Уведомления",
        "en": "🔔 Notifications",
        "uz": "🔔 Билдиришномалар",
        "uzl": "🔔 Bildirishnomalar",
    },

    "btn_about": {
        "ru": "ℹ️ О боте",
        "en": "ℹ️ About",
        "uz": "ℹ️ Бот ҳақида",
        "uzl": "ℹ️ Bot haqida",
    },

    "btn_basics": {
        "ru": "☦️ Основы православия",
        "en": "☦️ Basics of Orthodoxy",
        "uz": "☦️ Православие асослари",
        "uzl": "☦️ Pravoslavie asoslari",
    },
    "btn_language": {
        "ru": "🌐 Язык",
        "en": "🌐 Language",
        "uz": "🌐 Тил",
        "uzl": "🌐 Til",
    },
    "btn_back": {
        "ru": "◀️ Назад",
        "en": "◀️ Back",
        "uz": "◀️ Орқага",
        "uzl": "◀️ Orqaga",
    },
    "send_location_prompt": {
        "ru": "📍 Отправьте вашу геолокацию — покажу ближайшие храмы.\n\n<i>Нажмите кнопку ниже или прикрепите геолокацию вручную.</i>",
        "en": "📍 Share your location — I'll show the nearest churches.\n\n<i>Press the button below or attach location manually.</i>",
        "uz": "📍 Жойлашувингизни юборинг — яқин черковларни кўрсатаман.\n\n<i>Қуйидаги тугмани босинг ёки жойлашувни қўлда бириктиринг.</i>",
        "uzl": "📍 Joylashuvingizni yuboring — yaqin cherkovlarni ko'rsataman.\n\n<i>Quyidagi tugmani bosing yoki joylashuvni qo'lda biriktiring.</i>",
    },
    "btn_share_location": {
        "ru": "📍 Отправить местоположение",
        "en": "📍 Share Location",
        "uz": "📍 Жойлашувни юбориш",
        "uzl": "📍 Joylashuvni yuborish",
    },
    "nearest_churches_result": {
        "ru": "🗺 Ближайшие храмы:",
        "en": "🗺 Nearest churches:",
        "uz": "🗺 Яқин черковлар:",
        "uzl": "🗺 Yaqin cherkovlar:",
    },
    "distance_km": {
        "ru": "{dist:.1f} км",
        "en": "{dist:.1f} km",
        "uz": "{dist:.1f} км",
        "uzl": "{dist:.1f} km",
    },
    "no_churches_found": {
        "ru": "Храмы не найдены. Попробуйте выбрать город вручную.",
        "en": "No churches found. Try selecting a city manually.",
        "uz": "Черковлар топилмади. Шаҳарни қўлда танлаб кўринг.",
        "uzl": "Cherkovlar topilmadi. Shahanni qo'lda tanlab ko'ring.",
    },
    "choose_city": {
        "ru": "🏙 Выберите город:",
        "en": "🏙 Choose a city:",
        "uz": "🏙 Шаҳарни танланг:",
        "uzl": "🏙 Shahanni tanlang:",
    },
    "choose_church": {
        "ru": "Выберите храм:",
        "en": "Choose a church:",
        "uz": "Черковни танланг:",
        "uzl": "Cherkovni tanlang:",
    },
    "church_detail": {
        "ru": "⛪ <b>{name}</b>\n📌 {address}\n{phone_line}\n{description}",
        "en": "⛪ <b>{name}</b>\n📌 {address}\n{phone_line}\n{description}",
        "uz": "⛪ <b>{name}</b>\n📌 {address}\n{phone_line}\n{description}",
        "uzl": "⛪ <b>{name}</b>\n📌 {address}\n{phone_line}\n{description}",
    },
    "church_phone": {
        "ru": "📞 {phone}\n",
        "en": "📞 {phone}\n",
        "uz": "📞 {phone}\n",
        "uzl": "📞 {phone}\n",
    },
    "btn_schedule": {
        "ru": "🕐 Расписание служб",
        "en": "🕐 Service Schedule",
        "uz": "🕐 Ибодат жадвали",
        "uzl": "🕐 Ibodat jadvali",
    },
    "btn_navigate_google": {
        "ru": "🗺 Google Maps",
        "en": "🗺 Google Maps",
        "uz": "🗺 Google Maps",
        "uzl": "🗺 Google Maps",
    },
    "btn_navigate_yandex": {
        "ru": "🗺 Яндекс.Карты",
        "en": "🗺 Yandex Maps",
        "uz": "🗺 Яндекс.Харита",
        "uzl": "🗺 Yandex.Xarita",
    },
    "schedule_header": {
        "ru": "🕐 <b>Расписание служб</b>\n⛪ {church}\n\nНеделя {start} – {end}:\n",
        "en": "🕐 <b>Service Schedule</b>\n⛪ {church}\n\nWeek {start} – {end}:\n",
        "uz": "🕐 <b>Ибодат жадвали</b>\n⛪ {church}\n\nҲафта {start} – {end}:\n",
        "uzl": "🕐 <b>Ibodat jadvali</b>\n⛪ {church}\n\nHafta {start} – {end}:\n",
    },
    "schedule_day_header": {
        "ru": "\n<b>{weekday}, {date}</b>",
        "en": "\n<b>{weekday}, {date}</b>",
        "uz": "\n<b>{weekday}, {date}</b>",
        "uzl": "\n<b>{weekday}, {date}</b>",
    },
    "schedule_entry": {
        "ru": "  • {time} — {service}{notes}",
        "en": "  • {time} — {service}{notes}",
        "uz": "  • {time} — {service}{notes}",
        "uzl": "  • {time} — {service}{notes}",
    },
    "schedule_notes": {
        "ru": " <i>({notes})</i>",
        "en": " <i>({notes})</i>",
        "uz": " <i>({notes})</i>",
        "uzl": " <i>({notes})</i>",
    },
    "schedule_no_services": {
        "ru": "  <i>Служб не запланировано</i>",
        "en": "  <i>No services scheduled</i>",
        "uz": "  <i>Ибодатлар режалаштирилмаган</i>",
        "uzl": "  <i>Ibodatlar rejalashtirilmagan</i>",
    },
    # Calendar
    "calendar_today": {
        "ru": "📅 <b>Православный календарь</b>\n<b>{date}</b>  •  {weekday}\n{tone_line}\n🕊 <b>Праздник / Память:</b>\n{feast}\n\n📖 <b>Чтения:</b>\n{readings}\n\n🌿 <b>Пост:</b> {fast}\n\n👤 <b>Святые дня:</b>\n{saints}",
        "en": "📅 <b>Orthodox Calendar</b>\n<b>{date}</b>  •  {weekday}\n{tone_line}\n🕊 <b>Feast / Commemoration:</b>\n{feast}\n\n📖 <b>Readings:</b>\n{readings}\n\n🌿 <b>Fast:</b> {fast}\n\n👤 <b>Saints of the day:</b>\n{saints}",
        "uz": "📅 <b>Православ тақвими</b>\n<b>{date}</b>  •  {weekday}\n{tone_line}\n🕊 <b>Байрам / Хотира:</b>\n{feast}\n\n📖 <b>Ўқишлар:</b>\n{readings}\n\n🌿 <b>Рўза:</b> {fast}\n\n👤 <b>Бугунги муқаддаслар:</b>\n{saints}",
        "uzl": "📅 <b>Pravoslav taqvimi</b>\n<b>{date}</b>  •  {weekday}\n{tone_line}\n🕊 <b>Bayram / Xotira:</b>\n{feast}\n\n📖 <b>O'qishlar:</b>\n{readings}\n\n🌿 <b>Ro'za:</b> {fast}\n\n👤 <b>Bugungi muqaddaslar:</b>\n{saints}",
    },
    "calendar_tone": {
        "ru": "🎵 <i>Глас {n}</i>\n",
        "en": "🎵 <i>Tone {n}</i>\n",
        "uz": "🎵 <i>Оҳанг {n}</i>\n",
        "uzl": "🎵 <i>Ohang {n}</i>\n",
    },
    "calendar_no_data": {
        "ru": "Данные календаря временно недоступны.",
        "en": "Calendar data is temporarily unavailable.",
        "uz": "Тақвим маълумотлари вақтинча мавжуд эмас.",
        "uzl": "Taqvim ma'lumotlari vaqtincha mavjud emas.",
    },
    "btn_cal_prev": {
        "ru": "◀ Вчера",
        "en": "◀ Yesterday",
        "uz": "◀ Кеча",
        "uzl": "◀ Kecha",
    },
    "btn_cal_next": {
        "ru": "Завтра ▶",
        "en": "Tomorrow ▶",
        "uz": "Эртага ▶",
        "uzl": "Ertaga ▶",
    },
    "btn_cal_today": {
        "ru": "● Сегодня",
        "en": "● Today",
        "uz": "● Бугун",
        "uzl": "● Bugun",
    },
    "btn_cal_week": {
        "ru": "📅 Неделя",
        "en": "📅 Week",
        "uz": "📅 Ҳафта",
        "uzl": "📅 Hafta",
    },
    "calendar_week_header": {
        "ru": "📅 <b>Неделя {start} – {end}</b>\n",
        "en": "📅 <b>Week {start} – {end}</b>\n",
        "uz": "📅 <b>Ҳафта {start} – {end}</b>\n",
        "uzl": "📅 <b>Hafta {start} – {end}</b>\n",
    },
    "calendar_week_day": {
        "ru": "\n<b>{weekday} {date}</b>\n{feast}\n🌿 {fast}",
        "en": "\n<b>{weekday} {date}</b>\n{feast}\n🌿 {fast}",
        "uz": "\n<b>{weekday} {date}</b>\n{feast}\n🌿 {fast}",
        "uzl": "\n<b>{weekday} {date}</b>\n{feast}\n🌿 {fast}",
    },
    "notifications_on": {
        "ru": "🔔 Ежедневные уведомления <b>включены</b>.\nКаждое утро вы получите сводку дня.",
        "en": "🔔 Daily notifications <b>enabled</b>.\nYou'll receive a morning briefing every day.",
        "uz": "🔔 Кунлик билдиришномалар <b>ёқилган</b>.\nҲар куни эрталаб кун хулосасини оласиз.",
        "uzl": "🔔 Kunlik bildirishnomalar <b>yoqilgan</b>.\nHar kuni ertalab kun xulosasini olasiz.",
    },
    "notifications_off": {
        "ru": "🔕 Ежедневные уведомления <b>отключены</b>.",
        "en": "🔕 Daily notifications <b>disabled</b>.",
        "uz": "🔕 Кунлик билдиришномалар <b>ўчирилган</b>.",
        "uzl": "🔕 Kunlik bildirishnomalar <b>o'chirilgan</b>.",
    },
    "ask_question_prompt": {
        "ru": "✉️ <b>Написать в епархию</b>\n\nНапишите ваш вопрос. Администрация ответит в меру возможностей.\n\n<i>Ответ придёт сюда. Время ответа не гарантировано.\nПовторный вопрос — не ранее чем через 24 часа.</i>",
        "en": "✉️ <b>Write to the Diocese</b>\n\nType your question. The administration will reply when possible.\n\n<i>The reply will come here. Response time is not guaranteed.\nNext question allowed after 24 hours.</i>",
        "uz": "✉️ <b>Епархияга ёзиш</b>\n\nСаволингизни ёзинг. Маъмурият имкон қадар жавоб беради.\n\n<i>Жавоб шу ерга келади. Жавоб вақти кафолатланмаган.\nКейинги савол — 24 соатдан кейин.</i>",
        "uzl": "✉️ <b>Yeparxiyaga yozish</b>\n\nSavolingizni yozing. Ma'muriyat imkon qadar javob beradi.\n\n<i>Javob shu yerga keladi. Javob vaqti kafolatlanmagan.\nKeyingi savol — 24 soatdan keyin.</i>",
    },
    "question_sent": {
        "ru": "✅ Ваше сообщение отправлено. Благодарим за обращение.",
        "en": "✅ Your message has been sent. Thank you for reaching out.",
        "uz": "✅ Хабарингиз юборилди. Мурожаатингиз учун раҳмат.",
        "uzl": "✅ Xabaringiz yuborildi. Murojatingiz uchun rahmat.",
    },
    "question_cooldown": {
        "ru": "⏳ Следующий вопрос можно задать через {hours} ч.",
        "en": "⏳ You can ask again in {hours} h.",
        "uz": "⏳ Кейинги саволни {hours} соатдан кейин бериш мумкин.",
        "uzl": "⏳ Keyingi savolni {hours} soatdan keyin berish mumkin.",
    },
    "btn_cancel": {
        "ru": "❌ Отмена",
        "en": "❌ Cancel",
        "uz": "❌ Бекор қилиш",
        "uzl": "❌ Bekor qilish",
    },
    "action_cancelled": {
        "ru": "Действие отменено.",
        "en": "Action cancelled.",
        "uz": "Амал бекор қилинди.",
        "uzl": "Amal bekor qilindi.",
    },
    "about": {
        "ru": "ℹ️ <b>О боте</b>\n\nПравославный помощник Ташкентской и Узбекистанской епархии.\n\n🌐 <a href='https://pravoslavie.uz'>pravoslavie.uz</a>\n📱 Официальный канал епархии в Telegram",
        "en": "ℹ️ <b>About</b>\n\nOrthodox assistant of the Tashkent and Uzbekistan Diocese.\n\n🌐 <a href='https://pravoslavie.uz'>pravoslavie.uz</a>\n📱 Official Diocese Telegram channel",
        "uz": "ℹ️ <b>Бот ҳақида</b>\n\nТошкент ва Ўзбекистон епархиясининг православ ёрдамчиси.\n\n🌐 <a href='https://pravoslavie.uz'>pravoslavie.uz</a>\n📱 Епархиянинг расмий Telegram канали",
        "uzl": "ℹ️ <b>Bot haqida</b>\n\nToshkent va O'zbekiston yeparxiyasining pravoslav yordamchisi.\n\n🌐 <a href='https://pravoslavie.uz'>pravoslavie.uz</a>\n📱 Yeparxiyaning rasmiy Telegram kanali",
    },
    "admin_menu": {
        "ru": "⚙️ <b>Панель управления</b>",
        "en": "⚙️ <b>Admin Panel</b>",
        "uz": "⚙️ <b>Бошқарув панели</b>",
        "uzl": "⚙️ <b>Boshqaruv paneli</b>",
    },
    "admin_btn_questions": {
        "ru": "✉️ Вопросы без ответа",
        "en": "✉️ Unanswered questions",
        "uz": "✉️ Жавобсиз саволлар",
        "uzl": "✉️ Javobsiz savollar",
    },
    "admin_btn_broadcast": {
        "ru": "📢 Рассылка",
        "en": "📢 Broadcast",
        "uz": "📢 Тарқатиш",
        "uzl": "📢 Tarqatish",
    },
    "admin_btn_edit_schedule": {
        "ru": "🕐 Редактировать расписание",
        "en": "🕐 Edit schedule",
        "uz": "🕐 Жадвални таҳрирлаш",
        "uzl": "🕐 Jadvalni tahrirlash",
    },
    "admin_no_questions": {
        "ru": "Нет неотвеченных вопросов.",
        "en": "No unanswered questions.",
        "uz": "Жавобсиз саволлар йўқ.",
        "uzl": "Javobsiz savollar yo'q.",
    },
    "admin_question_item": {
        "ru": "❓ <b>#{id}</b> от {user} ({date})\n{text}",
        "en": "❓ <b>#{id}</b> from {user} ({date})\n{text}",
        "uz": "❓ <b>#{id}</b> — {user} ({date})\n{text}",
        "uzl": "❓ <b>#{id}</b> — {user} ({date})\n{text}",
    },
    "admin_btn_answer": {
        "ru": "Ответить на #{id}",
        "en": "Answer #{id}",
        "uz": "#{id} га жавоб бериш",
        "uzl": "#{id} ga javob berish",
    },
    "admin_answer_prompt": {
        "ru": "Введите ответ на вопрос #{id}:",
        "en": "Enter answer to question #{id}:",
        "uz": "#{id} саволга жавоб киритинг:",
        "uzl": "#{id} savolga javob kiriting:",
    },
    "admin_answer_sent": {
        "ru": "✅ Ответ отправлен пользователю.",
        "en": "✅ Answer sent to the user.",
        "uz": "✅ Жавоб фойдаланувчига юборилди.",
        "uzl": "✅ Javob foydalanuvchiga yuborildi.",
    },
    "admin_broadcast_prompt": {
        "ru": "📢 Введите текст рассылки (поддерживается HTML):",
        "en": "📢 Enter broadcast text (HTML supported):",
        "uz": "📢 Тарқатиш матнини киритинг (HTML қўллаб-қувватланади):",
        "uzl": "📢 Tarqatish matnini kiriting (HTML qo'llab-quvvatlanadi):",
    },
    "admin_broadcast_confirm": {
        "ru": "Отправить следующее сообщение <b>{count}</b> пользователям?\n\n{text}",
        "en": "Send the following message to <b>{count}</b> users?\n\n{text}",
        "uz": "Қуйидаги хабарни <b>{count}</b> та фойдаланувчига юборилсинми?\n\n{text}",
        "uzl": "Quyidagi xabarni <b>{count}</b> ta foydalanuvchiga yuborilsinmi?\n\n{text}",
    },
    "admin_broadcast_done": {
        "ru": "✅ Рассылка завершена. Отправлено: {count}.",
        "en": "✅ Broadcast complete. Sent: {count}.",
        "uz": "✅ Тарқатиш якунланди. Юборилди: {count}.",
        "uzl": "✅ Tarqatish yakunlandi. Yuborildi: {count}.",
    },
    "admin_btn_confirm": {
        "ru": "✅ Подтвердить",
        "en": "✅ Confirm",
        "uz": "✅ Тасдиқлаш",
        "uzl": "✅ Tasdiqlash",
    },
    "not_authorized": {
        "ru": "⛔ Нет доступа.",
        "en": "⛔ Access denied.",
        "uz": "⛔ Рухсат йўқ.",
        "uzl": "⛔ Ruxsat yo'q.",
    },
    "answer_received": {
        "ru": "✉️ <b>Ответ на ваш вопрос:</b>\n\n{answer}",
        "en": "✉️ <b>Answer to your question:</b>\n\n{answer}",
        "uz": "✉️ <b>Саволингизга жавоб:</b>\n\n{answer}",
        "uzl": "✉️ <b>Savolingizga javob:</b>\n\n{answer}",
    },
    # Schedule period selector
    "choose_schedule_period": {
        "ru": "Выберите период расписания:",
        "en": "Choose schedule period:",
        "uz": "Жадвал даврини танланг:",
        "uzl": "Jadval davrini tanlang:",
    },
    "btn_today": {
        "ru": "📌 На сегодня",
        "en": "📌 Today",
        "uz": "📌 Бугунга",
        "uzl": "📌 Bugunga",
    },
    "btn_week": {
        "ru": "📅 На неделю",
        "en": "📅 This week",
        "uz": "📅 Ҳафтага",
        "uzl": "📅 Haftaga",
    },
    "no_schedule": {
        "ru": "На этот период расписание пока не добавлено.",
        "en": "No schedule has been added for this period yet.",
        "uz": "Бу давр учун жадвал ҳали қўшилмаган.",
        "uzl": "Bu davr uchun jadval hali qo'shilmagan.",
    },
    "schedule_header_today": {
        "ru": "📌 Расписание на сегодня:",
        "en": "📌 Today's schedule:",
        "uz": "📌 Бугунги жадвал:",
        "uzl": "📌 Bugungi jadval:",
    },
    "schedule_header_week": {
        "ru": "📅 Расписание на неделю:",
        "en": "📅 Weekly schedule:",
        "uz": "📅 Ҳафталик жадвал:",
        "uzl": "📅 Haftalik jadval:",
    },
    # Admin schedule management
    "admin_sch_choose_method": {
        "ru": "Выберите способ добавления расписания:",
        "en": "Choose how to add schedule entries:",
        "uz": "Жадвал қўшиш усулини танланг:",
        "uzl": "Jadval qo'shish usulini tanlang:",
    },
    "admin_sch_manual": {
        "ru": "✏️ Добавить вручную",
        "en": "✏️ Add manually",
        "uz": "✏️ Қўлда қўшиш",
        "uzl": "✏️ Qo'lda qo'shish",
    },
    "admin_sch_file": {
        "ru": "📎 Загрузить CSV",
        "en": "📎 Upload CSV",
        "uz": "📎 CSV юклаш",
        "uzl": "📎 CSV yuklash",
    },
    "admin_sch_enter_church_id": {
        "ru": "Введите ID храма:",
        "en": "Enter church ID:",
        "uz": "Черков ID рақамини киритинг:",
        "uzl": "Cherkov ID raqamini kiriting:",
    },
    "admin_sch_enter_date": {
        "ru": "Введите дату (ГГГГ-ММ-ДД):",
        "en": "Enter date (YYYY-MM-DD):",
        "uz": "Сана киритинг (ЙЙЙЙ-ОО-КК):",
        "uzl": "Sana kiriting (YYYY-MM-DD):",
    },
    "admin_sch_enter_time": {
        "ru": "Введите время (ЧЧ:ММ):",
        "en": "Enter time (HH:MM):",
        "uz": "Вақт киритинг (СС:ДД):",
        "uzl": "Vaqt kiriting (HH:MM):",
    },
    "admin_sch_enter_titles": {
        "ru": "Введите названия через | (ru|en|uz|uzl):",
        "en": "Enter titles separated by | (ru|en|uz|uzl):",
        "uz": "Номларни | орқали киритинг (ru|en|uz|uzl):",
        "uzl": "Nomlarni | orqali kiriting (ru|en|uz|uzl):",
    },
    "admin_sch_record_added": {
        "ru": "✅ Запись добавлена.",
        "en": "✅ Record added.",
        "uz": "✅ Ёзув қўшилди.",
        "uzl": "✅ Yozuv qo'shildi.",
    },
    "admin_sch_upload_csv_prompt": {
        "ru": "Загрузите CSV файл. Столбцы: church_id, date(YYYY-MM-DD), time(HH:MM), title_ru, title_en, title_uz, title_uzl",
        "en": "Upload a CSV file. Columns: church_id, date(YYYY-MM-DD), time(HH:MM), title_ru, title_en, title_uz, title_uzl",
        "uz": "CSV файл юклаш. Устунлар: church_id, date(YYYY-MM-DD), time(HH:MM), title_ru, title_en, title_uz, title_uzl",
        "uzl": "CSV fayl yuklash. Ustunlar: church_id, date(YYYY-MM-DD), time(HH:MM), title_ru, title_en, title_uz, title_uzl",
    },
    "admin_sch_csv_done": {
        "ru": "✅ Загружено записей: {count}. Ошибок: {errors}.",
        "en": "✅ Records loaded: {count}. Errors: {errors}.",
        "uz": "✅ Юкланди: {count} та ёзув. Хатолар: {errors}.",
        "uzl": "✅ Yuklandi: {count} ta yozuv. Xatolar: {errors}.",
    },
    "admin_sch_invalid_id": {
        "ru": "Неверный ID. Введите целое число.",
        "en": "Invalid ID. Enter an integer.",
        "uz": "Нотўғри ID. Бутун сон киритинг.",
        "uzl": "Noto'g'ri ID. Butun son kiriting.",
    },
    "admin_sch_invalid_date": {
        "ru": "Неверный формат даты. Используйте ГГГГ-ММ-ДД.",
        "en": "Invalid date format. Use YYYY-MM-DD.",
        "uz": "Нотўғри сана формати. ЙЙЙЙ-ОО-КК форматини ишлатинг.",
        "uzl": "Noto'g'ri sana formati. YYYY-MM-DD formatini ishlating.",
    },
    "admin_sch_invalid_time": {
        "ru": "Неверный формат времени. Используйте ЧЧ:ММ.",
        "en": "Invalid time format. Use HH:MM.",
        "uz": "Нотўғри вақт формати. СС:ДД форматини ишлатинг.",
        "uzl": "Noto'g'ri vaqt formati. HH:MM formatini ishlating.",
    },
}

WEEKDAY_NAMES: dict[str, list[str]] = {
    "ru": ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "uz": ["Душанба", "Сешанба", "Чоршанба", "Пайшанба", "Жума", "Шанба", "Якшанба"],
    "uzl": ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"],
}

FAST_LABELS: dict[str, dict[int, str]] = {
    "ru": {
        0: "Поста нет",
        1: "Пост (рыба разрешена)",
        2: "Строгий пост (без рыбы)",
        3: "Сухоядение",
        4: "Воздержание от мяса",
        5: "Без мяса и рыбы",
        6: "Великий пост — строгое сухоядение",
    },
    "en": {
        0: "No fast",
        1: "Fast (fish permitted)",
        2: "Strict fast (no fish)",
        3: "Xerophagy",
        4: "Abstinence from meat",
        5: "No meat or fish",
        6: "Great Lent — strict xerophagy",
    },
    "uz": {
        0: "Рўза йўқ",
        1: "Рўза (балиқ рухсат)",
        2: "Қатъий рўза (балиқсиз)",
        3: "Қуруқ таом",
        4: "Гўштдан тийилиш",
        5: "Гўшт ва балиқсиз",
        6: "Буюк рўза — қатъий қуруқ таом",
    },
    "uzl": {
        0: "Ro'za yo'q",
        1: "Ro'za (baliq ruxsat)",
        2: "Qat'iy ro'za (balivsiz)",
        3: "Quruq taom",
        4: "Go'shtdan tiyilish",
        5: "Go'sht va balivsiz",
        6: "Buyuk ro'za — qat'iy quruq taom",
    },
}


def weekday_name(weekday: int, lang: str) -> str:
    names = WEEKDAY_NAMES.get(lang) or WEEKDAY_NAMES["ru"]
    return names[weekday]


def fast_label(level: int, lang: str) -> str:
    labels = FAST_LABELS.get(lang) or FAST_LABELS["ru"]
    return labels.get(level, "—")


def t(key: str, lang: str = "ru", **kwargs: Any) -> str:
    entry = _STRINGS.get(key, {})
    text = entry.get(lang) or entry.get("ru") or f"[{key}]"
    if kwargs:
        text = text.format(**kwargs)
    return text
