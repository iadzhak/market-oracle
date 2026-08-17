import datetime as dt
from enum import StrEnum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field

from .base import Base, DateTimeNowField
from ..constants import FRESH_DELTA_MINUTES, MIN_CONFIDENCE, MAX_CONFIDENCE


class ForecastType(StrEnum):
    UP = "up"
    DOWN = "down"
    UNCERTAIN = "uncertain"


class Forecast(Base, table=True):
    __tablename__ = 'forecasts'

    id: int | None = Field(default=None, primary_key=True)
    token: str
    direction: ForecastType
    confidence: float = Field(ge=MIN_CONFIDENCE, le=MAX_CONFIDENCE)
    created_at: DateTimeNowField

    @classmethod
    async def get(cls, session: AsyncSession, **kwargs):
        stmt = select(cls).filter_by(**kwargs)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_fresh_forecast(cls, session: AsyncSession, token: str):
        now = dt.datetime.now(dt.timezone.utc)
        some_time_ago = now - dt.timedelta(minutes=FRESH_DELTA_MINUTES)
        stmt = select(cls).where(cls.token == token, cls.created_at >= some_time_ago)
        result = await session.execute(stmt)
        return result.scalars().first()
