import asyncio
import datetime as dt

from ..sources import NewsBaseSource, PriceBaseSource


class DataProcessor:

    DELTA_DAYS_PREDICT = 1

    def __init__(self, price_getter: PriceBaseSource, news_getter: NewsBaseSource) -> None:
        self.price_getter = price_getter
        self.news_getter = news_getter

    async def get_raw_data(self, token: str, date: dt.datetime | None = None):
        """
        Получает сырые ценовые и новостные данные для токена.
        Возвращает кортеж: ohlcv_raw, news_raw
        """
        date = date or dt.datetime.now()
        ohlcv_raw, news_raw = await asyncio.gather(
            self.price_getter.get_ohlcv_1h(token=token, date_to=date),
            self.news_getter.get_news(token=token, date_to=date)
        )
        return ohlcv_raw, news_raw

    async def get_actual_price(self, token: str, date: dt.datetime) -> float:
        """
        Возвращает актуальную цену закрытия по данным прогноза.
        То есть дата прогноза плюс дельта (1 день)
        """
        check_date = date + dt.timedelta(days=self.DELTA_DAYS_PREDICT)
        if check_date > dt.datetime.now():
            raise RuntimeError(f'Невозможно получить данные на {check_date}')
        ohlcv_raw = await self.price_getter.get_ohlcv_1h(token=token)
        return self.price_getter.parce_close_price_last(ohlcv_raw)

    def normalize_raw_data(self, ohlcv_raw, news_raw):
        """
        Нормализует сырые данные, возвращая MA-сигнал и.sentiment-метрики.
        Дополнительно возвращает цену закрытия.
        Возвращает кортеж: last_close, ma_signal, news_p, news_s
        """
        news_descriptions = self.news_getter.parse_articles(news_raw)
        close_prices = self.price_getter.parse_close_prices(ohlcv_raw)

        ma_signal = self.price_getter.calculate_normalized_ma(close_prices)
        last_close = close_prices[-1]
        news_p, news_s = self.news_getter.calculate_news_sentiment(news_descriptions)

        return last_close, ma_signal, news_p, news_s

    @property
    def price_getter_id(self) -> str:
        return self.price_getter.id

    @property
    def news_getter_id(self) -> str:
        return self.news_getter.id
