import argparse
import asyncio
import datetime as dt
from enum import StrEnum

from .core import Oracle
from .database import Session
from .lifespan import get_news_getter, get_price_getter, setup_db
from .settings import conf
from .utils import collect, perform_train


class MODES(StrEnum):
    COLLECT = 'collect'
    TRAIN = 'train'


async def main(args):
    price_getter = get_price_getter()
    news_getter = get_news_getter()
    await setup_db([price_getter.info(), news_getter.info()])
    async with Session() as session:
        if args.mode == MODES.COLLECT:
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
