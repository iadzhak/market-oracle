import datetime as dt
from abc import ABC, abstractmethod
from typing import Any


class NewsBaseSource(ABC):
    @abstractmethod
    async def get_news(self, token: str, date_to: dt.datetime | None = None) -> Any:
        """
        Возвращает новости по убыванию даты.
        На определенную в параметрах дату.
        """
        pass

    @abstractmethod
    def calculate_news_sentiment(self, news: list[str]) -> tuple[float, float]:
        """
        На вход подаются тексты по которым нужно вычислить средний сентимент.
        Возвращает два значения полярность и объективность.
        """
        pass

    @abstractmethod
    def parse_articles(self, data: Any) -> list[str]:
        """
        Возвращает список содержимого статей список.
        """


class PriceBaseSource(ABC):
    @abstractmethod
    async def get_ohlcv_1h(self, token: str, date_to: dt.datetime | None = None, limit: int = 20) -> Any:
        """
        Возвращает OHLCV данные с timestamp(ms) в порядке возрастания timestamp.
        На определенную в параметрах дату. Цены получаем относительно USDT.
        Можно ограничивать количество данных через limit, по-умолчанию 20.
        """

    @abstractmethod
    def calculate_normalized_ma(self, prices: list[float]) -> float:
        """
        На вход подаются цены для расчета MA в порядке возрастания timestamp.
        Вернет нормализованный сигнал тренда.
        """

    @abstractmethod
    def parse_close_prices(self, data: Any) -> list[float]:
        """
        Возвращает список цен закрытия из данных OHLCV
        """

    @abstractmethod
    def parce_close_price_last(self, data: Any) -> float:
        """
        Возвращает последнюю цену закрытия
        """

    @abstractmethod
    async def close(self) -> None:
        """Закрытие соединения при необходимости"""
