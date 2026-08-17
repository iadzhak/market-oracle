import datetime as dt

import ccxt.async_support as ccxt

TIMEFRAME_1H = '1h'

def get_exchange(exchange_id: str='binance', retries: int=3, delay: int=1000) -> ccxt.Exchange:
    exchange = getattr(ccxt, exchange_id)()
    exchange.options['maxRetriesOnFailure'] = retries
    exchange.options['maxRetriesOnFailureDelay'] = delay
    return exchange


async def get_ohlcv_1h(
        exchange: ccxt.Exchange,
        token: str,
        for_date: dt.datetime | None = None,
        limit: int = 20,
) -> list[list[int | float]]:
    """Возвращает OHLCV данные с timestamp(ms) в порядке возрастания timestamp."""
    symbol = f'{token.upper()}/USDT'
    date_from = for_date or dt.datetime.now() - dt.timedelta(hours=limit)
    since = int(date_from.timestamp() * 1000)  # integer milliseconds
    data_ohlcv = await exchange.fetch_ohlcv(symbol=symbol, timeframe=TIMEFRAME_1H, since=since, limit=limit)
    return data_ohlcv
