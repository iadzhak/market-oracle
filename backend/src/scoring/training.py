import asyncio
import itertools
import datetime as dt
import logging

from tqdm import tqdm

from ..constants import SOURCE_NEWSAPI, SOURCE_BINANCE
from ..models import Metric, RawData
from ..sources import NewsBaseSource, PriceBaseSource


async def prepare_training_data(tokens: list[str], dates: list[dt.datetime]):
    """
    Подготавливает тренировочные данные
    На вход подаем список токенов и дата время объектов
    """
    token_date_list = list(itertools.product(tokens, dates))
    for token, date in token_date_list:
        pass


async def get_result(price_getter: PriceBaseSource, token: str, forecast_date: dt.datetime) -> float:
    check_date = forecast_date + dt.timedelta(days=1)
    if check_date > dt.datetime.now():
        raise RuntimeError(f'Невозможно получить данные на {check_date}')
    ohlcv_raw = await price_getter.get_ohlcv_1h(token=token)
    return price_getter.parce_close_price_last(ohlcv_raw)


async def get_data(
        price_getter: PriceBaseSource,
        news_getter: NewsBaseSource,
        token: str,
        today: dt.datetime | None = None
) -> tuple[list[RawData], Metric]:
    today = today or dt.datetime.now()
    logging.info(f'Составлю прогноз на {today + dt.timedelta(days=1)}')
    ohlcv_raw, news_raw = asyncio.gather(
        price_getter.get_ohlcv_1h(token=token, date_to=today),
        news_getter.get_news(token=token, date_to=today)
    )

    news_descriptions = news_getter.parse_articles(news_raw)
    close_prices = price_getter.parse_close_prices(ohlcv_raw)

    ma_signal = price_getter.calculate_normalized_ma(close_prices)
    news_p, news_s = news_getter.calculate_news_sentiment(news_descriptions)

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


if __name__ == '__main__':
    asyncio.run(prepare_training_data(
        ['a', 'b'],
        [dt.datetime.now() - dt.timedelta(days=d) for d in [2,3,4]]
    ))


