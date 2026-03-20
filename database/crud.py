"""
CRUD helpers — thin wrappers around SQLAlchemy queries.
"""

from datetime import date, datetime, timedelta
from math import atan2, cos, radians, sin, sqrt
from typing import Optional

from sqlalchemy import select, and_, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.db import (
    Broadcast,
    Church,
    City,
    Question,
    Schedule,
    ServiceSchedule,
    User,
    async_session,
    get_session,
)


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

async def get_or_create_user(
    user_id: int,
    username: Optional[str],
    full_name: str,
    language: str = "ru",
) -> User:
    async with get_session() as session:
        user = await session.get(User, user_id)
        if user is None:
            user = User(
                id=user_id,
                username=username,
                full_name=full_name,
                language=language,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        else:
            user.last_seen = datetime.utcnow()
            if username:
                user.username = username
            await session.commit()
            await session.refresh(user)
        return user


async def set_user_language(user_id: int, lang: str) -> None:
    async with get_session() as session:
        await session.execute(update(User).where(User.id == user_id).values(language=lang))
        await session.commit()


async def set_user_notifications(user_id: int, enabled: bool) -> None:
    async with get_session() as session:
        user = await session.get(User, user_id)
        if user:
            user.notifications_enabled = enabled
            await session.commit()


async def get_all_users_for_broadcast() -> list[User]:
    async with get_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def get_users_with_notifications() -> list[User]:
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.notifications_enabled.is_(True))
        )
        return result.scalars().all()


# ---------------------------------------------------------------------------
# Cities & Churches
# ---------------------------------------------------------------------------

async def get_all_cities() -> list[City]:
    async with get_session() as session:
        result = await session.execute(select(City).order_by(City.name_ru))
        return result.scalars().all()


async def get_churches_by_city(city_id: int) -> list[Church]:
    async with get_session() as session:
        result = await session.execute(
            select(Church)
            .where(and_(Church.city_id == city_id, Church.is_active.is_(True)))
            .order_by(Church.name_ru)
        )
        return result.scalars().all()


async def get_church(church_id: int) -> Optional[Church]:
    async with get_session() as session:
        return await session.get(Church, church_id)


async def get_all_churches() -> list[Church]:
    async with get_session() as session:
        result = await session.execute(
            select(Church).where(Church.is_active.is_(True))
        )
        return result.scalars().all()


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres."""
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


async def get_churches_near(lat: float, lon: float, limit: int = 5) -> list[tuple[Church, float]]:
    churches = await get_all_churches()
    with_dist = [
        (c, haversine_km(lat, lon, float(c.latitude), float(c.longitude)))
        for c in churches
    ]
    with_dist.sort(key=lambda x: x[1])
    return with_dist[:limit]


# ---------------------------------------------------------------------------
# ServiceSchedule (date-based, for admin upload)
# ---------------------------------------------------------------------------

async def get_schedule(church_id: int, period: str) -> list[ServiceSchedule]:
    """Return ServiceSchedule records for a church — today or next 7 days."""
    async with async_session() as session:
        today = date.today()
        query = select(ServiceSchedule).where(ServiceSchedule.church_id == church_id)

        if period == "today":
            query = query.where(ServiceSchedule.date == today)
        elif period == "week":
            end_date = today + timedelta(days=7)
            query = query.where(
                ServiceSchedule.date >= today,
                ServiceSchedule.date <= end_date,
            )

        result = await session.execute(query.order_by(ServiceSchedule.date, ServiceSchedule.time))
        return result.scalars().all()


async def add_schedule_record(data: dict) -> None:
    """Insert a raw ServiceSchedule row (used by admin CSV upload and manual entry)."""
    async with async_session() as session:
        obj = ServiceSchedule(**data)
        session.add(obj)
        await session.commit()


# ---------------------------------------------------------------------------
# Schedule (repeat-weekly logic, for the weekly view)
# ---------------------------------------------------------------------------

async def get_schedules_for_church_week(
    church_id: int, start_date: date
) -> list[Schedule]:
    """Return all Schedule entries for a church over 7 days starting from start_date."""
    end_date = start_date + timedelta(days=6)
    weekdays = [(start_date + timedelta(days=i)).weekday() for i in range(7)]

    async with get_session() as session:
        result = await session.execute(
            select(Schedule)
            .where(
                Schedule.church_id == church_id,
                or_(
                    and_(
                        Schedule.repeat_weekly.is_(True),
                        Schedule.weekday.in_(weekdays),
                    ),
                    and_(
                        Schedule.specific_date >= start_date,
                        Schedule.specific_date <= end_date,
                    ),
                ),
            )
            .order_by(Schedule.service_time)
        )
        return result.scalars().all()


async def add_schedule_entry(
    church_id: int,
    schedule_type_id: int,
    service_name_ru: str,
    service_name_en: str,
    service_time_str: str,
    repeat_weekly: bool,
    weekday: Optional[int],
    specific_date: Optional[date],
    notes_ru: Optional[str],
    notes_en: Optional[str],
    updated_by: int,
) -> Schedule:
    from datetime import time as dtime
    h, m = map(int, service_time_str.split(":"))
    stime = dtime(hour=h, minute=m)

    async with get_session() as session:
        entry = Schedule(
            church_id=church_id,
            schedule_type_id=schedule_type_id,
            service_name_ru=service_name_ru,
            service_name_en=service_name_en,
            service_time=stime,
            repeat_weekly=repeat_weekly,
            weekday=weekday,
            specific_date=specific_date,
            notes_ru=notes_ru,
            notes_en=notes_en,
            updated_by=updated_by,
        )
        session.add(entry)
        await session.commit()
        return entry


async def delete_schedule_entry(entry_id: int) -> bool:
    async with get_session() as session:
        entry = await session.get(Schedule, entry_id)
        if entry is None:
            return False
        await session.delete(entry)
        await session.commit()
        return True


# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------

async def create_question(user_id: int, text: str) -> Question:
    async with get_session() as session:
        q = Question(user_id=user_id, text=text)
        session.add(q)
        await session.commit()
        return q


async def get_unanswered_questions() -> list[Question]:
    async with get_session() as session:
        result = await session.execute(
            select(Question)
            .options(selectinload(Question.user))
            .where(Question.is_answered.is_(False))
            .order_by(Question.created_at)
        )
        return result.scalars().all()


async def answer_question(
    question_id: int, answer_text: str, answered_by: int
) -> Optional[Question]:
    async with get_session() as session:
        q = await session.get(Question, question_id, options=[selectinload(Question.user)])
        if q is None:
            return None
        q.is_answered = True
        q.answer_text = answer_text
        q.answered_at = datetime.utcnow()
        q.answered_by = answered_by
        await session.commit()
        return q


async def get_last_question_time(user_id: int) -> Optional[datetime]:
    async with get_session() as session:
        result = await session.execute(
            select(Question.created_at)
            .where(Question.user_id == user_id)
            .order_by(Question.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


# ---------------------------------------------------------------------------
# Broadcasts
# ---------------------------------------------------------------------------

async def create_broadcast(text: str, created_by: int) -> Broadcast:
    async with get_session() as session:
        b = Broadcast(text=text, created_by=created_by)
        session.add(b)
        await session.commit()
        return b


async def mark_broadcast_sent(broadcast_id: int, count: int) -> None:
    async with get_session() as session:
        b = await session.get(Broadcast, broadcast_id)
        if b:
            b.sent_at = datetime.utcnow()
            b.recipient_count = count
            await session.commit()
