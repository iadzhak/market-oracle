import asyncio
import itertools
import datetime as dt
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from tqdm import tqdm

from ..models import Forecast
from ..constants import SOURCE_NEWSAPI, SOURCE_BINANCE
from ..models import Metric, RawData
from ..sources import NewsBaseSource, PriceBaseSource


async def prepare_training_data(
        session: AsyncSession,
        price_getter: PriceBaseSource,
        news_getter: NewsBaseSource,
        tokens: list[str],
        dates: list[dt.datetime]
):
    """
    Подготавливает тренировочные данные
    На вход подаем список токенов и дата время объектов
    """
    token_date_list = list(itertools.product(tokens, dates))
    for token, date in tqdm(token_date_list):
        # get data, get result
        response = await asyncio.gather(
            get_data(price_getter, news_getter, token, date),
            get_result(price_getter, token, date)
        )
        raw_data, metric = response[0]
        result = response[1]
        forecast = Forecast(

        )
        # save raw, metrics and forecast
        session.add_all(raw_data)
        session.add(metric)
        # init ML
        # run education
        # save weights as default
    for token, date in token_date_list:
        print(token, date)

