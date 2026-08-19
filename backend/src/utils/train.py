from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import Oracle
from ..models import Forecast


async def perform_train(oracle: Oracle, session: AsyncSession):
    stmt = select(Forecast).where(Forecast.is_trained.is_(False), Forecast.actual.is_not(None))
    result = await session.execute(stmt)
    forecasts = result.scalars().all()
    x_train = [[f.price_ma_ratio, f.news_polarity, f.news_subjectivity] for f in forecasts]
    y_train = [f.actual for f in forecasts]
    oracle.train(x_train, y_train)
    for forecast in forecasts:
        x = [forecast.price_ma_ratio, forecast.news_polarity, forecast.news_subjectivity]
        pred, proba = oracle.predict([x])
        forecast.target = pred
        forecast.confidence = proba
        forecast.is_trained = True
    await session.commit()
