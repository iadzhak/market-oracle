import asyncio
import argparse
import datetime as dt
from pathlib import Path

from .database import get_session
from .scoring.training import prepare_training_data
from .settings import conf
from .sources import CCXTPriceGetter, NewsApiGetter
from .settings import conf

async def main():
    # define getters, session and oracle
    price_getter = CCXTPriceGetter(conf.CCXT_EXCHANGE)
    news_getter = NewsApiGetter(
        base_url=conf.NEWS_API_URL,
        api_key=conf.NEWS_API_KEY,
        news_url=conf.NEWS_API_ENDPOINT
    )
    session = get_session()
    # get raw_data and calculate metrics
    # OR
    # load metrics from file
    # create forecasts
    # save to db
    # train model
    print('hi')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Базовая тренировка модели')
    parser.add_argument('-f', '--file', default=None, help='file')
    args = parser.parse_args()
    if args.file:
        abs_path = Path(args.file).resolve()
        print(abs_path)
    print(args)
    asyncio.run(main())