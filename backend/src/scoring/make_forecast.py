from ..coingecko import download_history
from ..models import RawData, Metric
from ..constants import SOURCE_COINGECKO

async def make_forecast(token: str):
    raw_data = []

    ohlc_data = await download_history(token)
    if len(ohlc_data) < 40:
        raise ValueError('Недостаточно свечей для расчёта MA40')

    raw_data.append(
        RawData(
            source_id=SOURCE_COINGECKO,
            symbol=token,
            payload=ohlc_data
        )
    )
    closes = [c[4] for c in ohlc_data[-20:]]
    print(closes)
    sma40 = sum(closes) / len(closes)
    current_close = closes[-1]
    trend_up = current_close > sma40

    metric = Metric(
        close_last=current_close,
        ma_40=sma40
    )

    return raw_data, metric, trend_up
