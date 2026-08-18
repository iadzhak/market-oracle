import datetime as dt
from typing import Any

import ccxt.async_support as ccxt

from .base import PriceBaseSource


class CCXTPriceGetter(PriceBaseSource):

    TIMEFRAME_1H = '1h'

    def __init__(self, exchange_id: str, retries: int=3, delay: int=1000) -> None:
        self.exchange = getattr(ccxt, exchange_id)()
        self.exchange.options['maxRetriesOnFailure'] = retries
        self.exchange.options['maxRetriesOnFailureDelay'] = delay

    async def get_ohlcv_1h(self, token: str, date_to: dt.datetime | None = None, limit: int = 20) -> Any:
        symbol = f'{token.upper()}/USDT'
        date_from = date_to or dt.datetime.now()
        date_from -= dt.timedelta(hours=limit)
        since = int(date_from.timestamp() * 1000)  # integer milliseconds
        data_ohlcv = await self.exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=self.TIMEFRAME_1H,
            since=since,
            limit=limit
        )
        return data_ohlcv

    def calculate_normalized_ma(self, prices: list[float]) -> float:
        if len(prices) == 0:
            return 0
        ma = sum(prices) / len(prices)
        return prices[-1] / ma - 1

    def parse_close_prices(self, data: Any) -> list[float]:
        return [d[4] for d in data]

    def parce_close_price_last(self, data: Any) -> float:
        return data[-1][4]

    async def close(self):
        await self.exchange.close()
