import asyncio
import argparse
from enum import StrEnum
import datetime as dt

from .core import Oracle
from .database import Session
from .sources import CCXTPriceGetter, NewsApiGetter
from .settings import conf
from .lifespan import setup_db, get_price_getter, get_news_getter
from .utils import collect, perform_train


class MODES(StrEnum):
    COLLECT = 'collect'
    TRAIN = 'train'


async def main(args):
    await setup_db()
    async with Session() as session:
        if args.mode == MODES.COLLECT:
            price_getter = get_price_getter()
            news_getter = get_news_getter()
            now = dt.datetime.now()
            dates = [now - dt.timedelta(days=x) for x in range(args.days + 2, 2, -1)]
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
    parser.add_argument(
        'mode', choices=MODES,
        help='Режим работы. collect - сбор данных и сохранение в бд. train - тренировка модели'
    )
    parser.add_argument(
        '-d', '--days',
        default=5, type=int,
        help='Дней для загружаемой выборки (collect mode, default=5)')
    args = parser.parse_args()
    asyncio.run(main(args))
