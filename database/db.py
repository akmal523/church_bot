"""
Database — SQLAlchemy async models + Alembic-ready metadata
"""

from datetime import datetime, date, time
from typing import Optional
from sqlalchemy import (
    BigInteger, Boolean, Date, DateTime, ForeignKey,
    Integer, Numeric, String, Text, Time, func, Column
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

class ServiceSchedule(Base):
    __tablename__ = "service_schedules"
    id = Column(Integer, primary_key=True, index=True)
    church_id = Column(Integer, ForeignKey("churches.id"))
    date = Column(Date, index=True)
    time = Column(String)
    title_ru = Column(String)
    title_en = Column(String)
    title_uz = Column(String)
    title_uzl = Column(String)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(64))
    full_name: Mapped[str] = mapped_column(String(128))
    language: Mapped[str] = mapped_column(String(4), default="ru")
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    questions: Mapped[list["Question"]] = relationship(back_populates="user")

class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_ru: Mapped[str] = mapped_column(String(64))
    name_en: Mapped[str] = mapped_column(String(64))
    name_uz: Mapped[Optional[str]] = mapped_column(String(64))
    name_uzl: Mapped[Optional[str]] = mapped_column(String(64))
    churches: Mapped[list["Church"]] = relationship(back_populates="city")

class Church(Base):
    __tablename__ = "churches"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    name_ru: Mapped[str] = mapped_column(String(128))
    name_en: Mapped[str] = mapped_column(String(128))
    name_uz: Mapped[Optional[str]] = mapped_column(String(128))
    name_uzl: Mapped[Optional[str]] = mapped_column(String(128))
    address_ru: Mapped[str] = mapped_column(String(256))
    address_en: Mapped[str] = mapped_column(String(256))
    address_uz: Mapped[Optional[str]] = mapped_column(String(256))
    address_uzl: Mapped[Optional[str]] = mapped_column(String(256))
    latitude: Mapped[float] = mapped_column(Numeric(10, 7))
    longitude: Mapped[float] = mapped_column(Numeric(10, 7))
    phone: Mapped[Optional[str]] = mapped_column(String(32))
    description_ru: Mapped[Optional[str]] = mapped_column(Text)
    description_en: Mapped[Optional[str]] = mapped_column(Text)
    description_uz: Mapped[Optional[str]] = mapped_column(Text)
    description_uzl: Mapped[Optional[str]] = mapped_column(Text)
    google_maps_url: Mapped[Optional[str]] = mapped_column(String(512))
    yandex_maps_url: Mapped[Optional[str]] = mapped_column(String(512))
    patron_feast_date: Mapped[Optional[date]] = mapped_column(Date)
    admin_telegram_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    city: Mapped["City"] = relationship(back_populates="churches")
    schedules: Mapped[list["Schedule"]] = relationship(back_populates="church")

class ScheduleType(Base):
    __tablename__ = "schedule_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_ru: Mapped[str] = mapped_column(String(64))
    name_en: Mapped[str] = mapped_column(String(64))

class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    church_id: Mapped[int] = mapped_column(ForeignKey("churches.id"))
    schedule_type_id: Mapped[int] = mapped_column(ForeignKey("schedule_types.id"))
    service_name_ru: Mapped[str] = mapped_column(String(128))
    service_name_en: Mapped[str] = mapped_column(String(128))
    service_time: Mapped[time] = mapped_column(Time)
    specific_date: Mapped[Optional[date]] = mapped_column(Date, index=True)
    repeat_weekly: Mapped[bool] = mapped_column(Boolean, default=False)
    weekday: Mapped[Optional[int]] = mapped_column(Integer)
    notes_ru: Mapped[Optional[str]] = mapped_column(String(256))
    notes_en: Mapped[Optional[str]] = mapped_column(String(256))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    updated_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    church: Mapped["Church"] = relationship(back_populates="schedules")

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_answered: Mapped[bool] = mapped_column(Boolean, default=False)
    answer_text: Mapped[Optional[str]] = mapped_column(Text)
    answered_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    answered_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    user: Mapped["User"] = relationship(back_populates="questions")

class Broadcast(Base):
    __tablename__ = "broadcasts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    recipient_count: Mapped[int] = mapped_column(Integer, default=0)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_session() -> AsyncSession:
    return async_session()
