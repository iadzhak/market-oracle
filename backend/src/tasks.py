import logging

from .core import Oracle
from .dependencies import DataProcessorDep, SessionDep
from .models import Forecast

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


async def perform_partial_fit(token: str, session: SessionDep, data_processor: DataProcessorDep):
    logger.info(f'[{token}] Проверю пора ли на тренировку')
    not_trained: list[Forecast] = await Forecast.get_not_trained(session, token)
    if len(not_trained) < 5:
        logger.info(f'[{token}] Данных маловато')
        return
    x_train, y_train = [], []
    for f in not_trained:
        actual_price = await data_processor.get_actual_price(token, f.created_at)
        f.actual = 1 if actual_price > f.last_price else 0
        f.is_trained = True
        x_train.append([f.price_ma_ratio, f.news_polarity, f.news_subjectivity])
        y_train.append(f.actual)
    oracle = Oracle(token)
    oracle.train(x_train, y_train)
    await session.commit()
    logger.info(f'[{token}] Тренировка прошла успешно')
