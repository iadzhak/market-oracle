import asyncio

from ..coingecko import download_history
from ..models import RawData, Metric, ForecastType, Forecast
from ..constants import SOURCE_COINGECKO, SOURCE_WORLDNEWS
from ..worldnews import get_news
from ..settings import conf

async def make_forecast(token: str):
    ohlc_data, news_data = await asyncio.gather(
        download_history(token),
        get_news(conf.TOKENS_AND_SEARCH[token])
    )

    if len(ohlc_data) < 40:
        raise ValueError('Недостаточно свечей для расчёта MA40')

    raw_data = [
        RawData(
            source_id=SOURCE_COINGECKO,
            symbol=token,
            payload=ohlc_data
        ),
        RawData(
            source_id=SOURCE_WORLDNEWS,
            symbol=token,
            payload=news_data
        )
    ]

    closes = [c[4] for c in ohlc_data[-20:]]
    sma40 = sum(closes) / len(closes)
    current_close = closes[-1]
    trend_up = current_close > sma40

    news_sentiments = [
        float(n['sentiment'])
        for n in news_data.get('news',[])
        if n['sentiment'] is not None
    ]
    news_total_sentiment = sum(news_sentiments)
    news_count = len(news_sentiments)
    news_avg_sent = news_total_sentiment / news_count

    score = (1.0 if trend_up else -1.0) + 0.5 * news_avg_sent

    metric = Metric(
        close_last=current_close,
        ma_40=sma40,
        news_total_sentiment=news_total_sentiment,
        news_count=news_count,
        score=score,
    )

    if score > 0.3:
        direction = ForecastType.UP
    elif score < -0.3:
        direction = ForecastType.DOWN
    else:
        direction = ForecastType.UNCERTAIN

    result = Forecast(
        token=token,
        direction=direction,
        confidence=0
    )

    return raw_data, metric, result
