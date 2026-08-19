import datetime as dt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field, Relationship

from ..constants import FRESH_DELTA_MINUTES
from .base import Base, DateTimeNowField


class Forecast(Base, table=True):
    __tablename__ = 'forecasts'

    id: int | None = Field(default=None, primary_key=True)
    token: str
    last_price: float
    target: float | None = Field(default=None)
    confidence: float | None = Field(default=None)
    actual: int | None = Field(default=None)  # 0 - вниз, 1 - вверх
    price_ma_ratio: float
    news_polarity: float
    news_subjectivity: float
    created_at: DateTimeNowField
    is_trained: bool = Field(default=False)

    raw_data: list['RawData'] = Relationship(back_populates='forecast')

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

    @classmethod
    async def get_error_raito(cls, session: AsyncSession, token: str) -> float:
        token = token.upper()
        stmt = select(cls).where(cls.token == token, cls.target.is_not(None), cls.actual.is_not(None))
        result = await session.execute(stmt)
        forecasts = result.scalars().all()
        if len(forecasts) == 0:
            return 0
        wrong = 0
        for forecast in forecasts:
            if forecast.target != forecast.actual:
                wrong += 1
        return wrong / len(forecasts)
