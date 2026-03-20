# Orthodox Bot — Uzbekistan

A Telegram bot for Orthodox Christians in Uzbekistan. Provides service schedules, the Orthodox calendar, nearest church search, and a direct channel to the diocese — in four languages.

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Bot framework | aiogram 3.x |
| Database | PostgreSQL (SQLAlchemy async + asyncpg) |
| Calendar data | Offline JSON (`locales/saints.json`) |
| HTTP client | aiohttp |
| Config | pydantic-settings (`.env`) |

---

## Features

### User
| Feature | Description |
|---|---|
| **Nearest church** | Share location → sorted list with Google Maps / Yandex Maps links |
| **Browse by city** | Tashkent, Samarkand, Bukhara, Fergana, Nukus, and 27 more cities |
| **Weekly schedule** | Per-church, weekday / Sunday / feast separation |
| **Orthodox calendar** | Today's feast, fast level, saint of the day |
| **Write to diocese** | Rate-limited question form (1 per 24 h), answer returned in chat |
| **Basics of Orthodoxy** | Multilingual catechism chapters |
| **Daily notifications** | Opt-in morning briefing at 07:00 |
| **4 languages** | Russian · English · Uzbek Cyrillic · Uzbek Latin |

### Admin (`/admin` command)
| Feature | Description |
|---|---|
| **Questions** | View unanswered questions, reply (answer forwarded to user) |
| **Broadcast** | Mass message with preview + confirmation, rate-limited |
| **Schedule** | Add entries manually (FSM) or via CSV upload |

Admin access is controlled by `ADMIN_IDS` in `.env`.

---

## Project structure

```
orthodox_bot/
├── main.py                  # Entry point — dispatcher, scheduler
├── config.py                # Settings from .env (pydantic-settings)
├── seed.py                  # One-time DB seed (cities + churches)
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── database/
│   ├── db.py                # SQLAlchemy models + engine
│   └── crud.py              # All DB queries
├── handlers/
│   ├── start.py             # /start, language selection, main menu
│   ├── churches.py          # Geolocation + city/church browse
│   ├── schedule.py          # Service schedule (weekly + date-based views)
│   ├── calendar.py          # Orthodox calendar (today)
│   ├── questions.py         # User → diocese messaging (with cooldown)
│   ├── broadcast.py         # Admin mass messaging
│   ├── admin.py             # Admin panel, answer questions
│   ├── admin_schedule.py    # Admin schedule editor (manual + CSV)
│   └── basics.py            # "Basics of Orthodoxy" reader
├── keyboards/
│   └── kb.py                # All inline / reply keyboards
├── locales/
│   ├── i18n.py              # All UI strings in ru / en / uz / uzl
│   ├── basics.json          # Catechism chapters content
│   └── saints.json          # Offline saints calendar (MM-DD keyed)
└── utils/
    ├── calendar_api.py      # Offline calendar + fast calculation
    ├── broadcaster.py       # Rate-limited mass send (25 msg/s)
    ├── middleware.py        # User language injection middleware
    └── scheduler.py        # Daily morning notifications (07:00)
```

---

## Setup

```bash
# 1. Clone
git clone https://github.com/akmal523/church_bot.git
cd church_bot

# 2. Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env — set BOT_TOKEN, DATABASE_URL, ADMIN_IDS

# 4. Create PostgreSQL database
createdb orthodox_bot

# 5. Seed initial data (cities + churches)
python seed.py

# 6. Run
python main.py
```

---

## Docker

```bash
cp .env.example .env
# Edit .env — set BOT_TOKEN, ADMIN_IDS, POSTGRES_PASSWORD

docker compose up -d
```

The `docker-compose.yml` reads all credentials from `.env`. No secrets are hardcoded.

---

## Configuration reference

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | Yes | Telegram Bot Token from @BotFather |
| `DATABASE_URL` | Yes | PostgreSQL async DSN (`postgresql+asyncpg://...`) |
| `ADMIN_IDS` | Yes | JSON list of Telegram user IDs, e.g. `[123456789]` |
| `GOOGLE_MAPS_API_KEY` | No | Only needed for advanced map features |
| `QUESTION_COOLDOWN_HOURS` | No | Default: `24` |
| `POSTGRES_USER` | Docker | Default: `postgres` |
| `POSTGRES_PASSWORD` | Docker | Required — no default |
| `POSTGRES_DB` | Docker | Default: `orthodox_bot` |

---

## Adding a new parish

Option 1 — add to `seed.py` and re-run:
```python
FULL_CHURCHES = [
    ...
    (city_index, "Название", "Name", "Ном (кирилл)", "Nom (lotin)",
     "Адрес RU", "Address EN", "Манзил UZ", "Manzil UZL",
     "+998 ...", "Описание RU", "Description EN", "Tavsif UZ", "Tavsif UZL",
     41.300, 69.240),
]
```

Option 2 — direct SQL:
```sql
INSERT INTO churches (city_id, name_ru, name_en, address_ru, address_en,
    latitude, longitude, google_maps_url, yandex_maps_url)
VALUES (24, 'Название', 'Name', 'Адрес', 'Address',
    41.300, 69.240,
    'https://maps.google.com/?q=41.300,69.240',
    'https://yandex.ru/maps/?pt=69.240,41.300&z=17');
```

---

## Adding schedule entries (admin)

**Via bot:** `/admin` → Edit schedule → Add manually (step-by-step FSM) or Upload CSV.

**CSV format:**
```
church_id,date,time,title_ru,title_en,title_uz,title_uzl
1,2025-01-07,09:00,Литургия,Liturgy,Литургия,Liturgiya
1,2025-01-07,17:00,Вечерня,Vespers,Вечерня,Vesper
```

---

## VPS deployment (systemd)

```ini
[Unit]
Description=Orthodox Bot
After=network.target postgresql.service

[Service]
User=botuser
WorkingDirectory=/home/botuser/orthodox_bot
EnvironmentFile=/home/botuser/orthodox_bot/.env
ExecStart=/home/botuser/venv/bin/python main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## Localization

All UI strings live in `locales/i18n.py` in the `_STRINGS` dict. Each key has entries for `ru`, `en`, `uz`, `uzl`.

To add a new language, extend every string entry and add the new code to `LANGS` and `WEEKDAY_NAMES`.

---

## License

MIT
