from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core import Oracle
from ..models import Forecast

async def perform_train(oracle: Oracle, session: AsyncSession):
    stmt = select(Forecast).where(Forecast.is_trained == False, Forecast.actual.is_not(None))
    result = await session.execute(stmt)
    forecasts = result.scalars().all()
    x_train = [[f.price_ma_ratio, f.news_polarity, f.news_subjectivity] for f in forecasts]
    y_train = [f.actual for f in forecasts]
    oracle.train(x_train, y_train)
