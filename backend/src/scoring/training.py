import asyncio
import datetime as dt
import logging

from ..constants import SOURCE_NEWSAPI, SOURCE_BINANCE
from ..models import Metric, RawData
from ..sources.prices_ccxt import get_ohlcv_1h
from ..sources.news_api import get_news
from .utils import calculate_normalized_ma_signal, calculate_news_sentiment


async def prepare_training_data():
    pass


async def get_data(
        token: str,
        exchange,
        client,
        today: dt.datetime | None = None
) -> tuple[list[RawData], Metric]:
    today = today or dt.datetime.now()
    logging.info(f'Составлю прогноз на {today + dt.timedelta(days=1)}')
    ohlcv_raw, news_raw = asyncio.gather(
        get_ohlcv_1h(
            exchange=exchange,
            token=token,
            for_date=today),
        get_news(
            token=token,
            date_to=today
        )
    )

    news_descriptions = [n['description'] for n in news_raw.get('articles', [])]
    ma_signal = calculate_normalized_ma_signal(ohlcv_raw)
    news_p, news_s = calculate_news_sentiment(news_descriptions)

    raw_data = [
        RawData(
            source_id=SOURCE_BINANCE,
            fetched_at=today,
            payload=ohlcv_raw
        ),
        RawData(
            source_id=SOURCE_NEWSAPI,
            fetched_at=today,
            payload=news_raw
        ),
    ]

    metric = Metric(
        ma=ma_signal,
        news_p=news_p,
        news_s=news_s,
        calculated_at=today
    )

    return raw_data, metric





