import asyncio
import datetime as dt
import itertools

from sqlalchemy.ext.asyncio import AsyncSession
from tqdm import tqdm

from ..models import Forecast, RawData
from ..sources import NewsBaseSource, PriceBaseSource
from .data import DataProcessor


async def collect(
        news_getter: NewsBaseSource,
        price_getter: PriceBaseSource,
        session: AsyncSession,
        tokens: list[str],
        dates: list[dt.datetime]
):
    token_dates = list(itertools.product(tokens, dates))
    data_processor = DataProcessor(price_getter=price_getter, news_getter=news_getter)
    for token, date in tqdm(token_dates):
        response = await asyncio.gather(
            data_processor.get_raw_data(token, date),
            data_processor.get_actual_price(token, date)
        )
        ohlcv_raw, news_raw = response[0]
        actual_price = response[1]
        last_close, ma_signal, news_p, news_s = data_processor.normalize_raw_data(ohlcv_raw, news_raw)

        actual = 1 if actual_price > last_close else 0

        forecast = Forecast(
            token=token,
            last_price=last_close,
            actual=actual,
            price_ma_ratio=ma_signal,
            news_polarity=news_p,
            news_subjectivity=news_s,
            created_at=date
        )
        ohlcv = RawData(
            source_id=data_processor.price_getter_id,
            fetched_at=date,
            payload=ohlcv_raw,
            forecast=forecast
        )
        news = RawData(
            source_id=data_processor.news_getter_id,
            fetched_at=date,
            payload=news_raw,
            forecast=forecast
        )

        session.add_all([forecast, ohlcv, news])
    await session.commit()
    print('Загрузка данных завершена')
