import asyncio
import argparse
from enum import StrEnum
import datetime as dt

from .core import Oracle
from .database import Session
from .sources import CCXTPriceGetter, NewsApiGetter
from .settings import conf
from .lifespan import setup_db
from .utils import collect, perform_train


class MODES(StrEnum):
    COLLECT = 'collect'
    TRAIN = 'train'


async def main(args):
    await setup_db()
    async with Session() as session:
        if args.mode == MODES.COLLECT:
            price_getter = CCXTPriceGetter(conf.CCXT_EXCHANGE)
            news_getter = NewsApiGetter(
                base_url=conf.NEWS_API_URL,
                api_key=conf.NEWS_API_KEY,
                news_url=conf.NEWS_API_ENDPOINT
            )
            now = dt.datetime.now()
            dates = [now - dt.timedelta(days=x) for x in range(7, 2, -1)]
            await collect(
                news_getter=news_getter,
                price_getter=price_getter,
                session=session,
                tokens=conf.TOKENS,
                dates=dates
            )
            await price_getter.close()
        elif args.mode == MODES.TRAIN:
            oracle = Oracle()
            await perform_train(oracle, session)
            print('Тренировка завершена')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Базовая тренировка модели')
    parser.add_argument('mode', choices=MODES, help='Режим работы')
    args = parser.parse_args()
    asyncio.run(main(args))
