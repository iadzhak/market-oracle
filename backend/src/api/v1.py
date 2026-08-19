from fastapi import APIRouter

from ..models import Forecast, RawData
from ..settings import conf
from ..dependencies import SessionDep, DataProcessorDep
from ..core import Oracle
from ..constants import SOURCE_NEWSAPI, SOURCE_BINANCE

router = APIRouter(prefix='/api')


@router.get('/tokens')
async def tokens() -> list[str]:
    return conf.TOKENS


@router.get('/tokens/{token}')
async def token_info(token: str, session: SessionDep, data_processor: DataProcessorDep):
    token = token.lower()
    forecast = await Forecast.get_fresh_forecast(session, token)
    if forecast is None:
        # get raw data and metrics
        ohlcv_raw, news_raw = await data_processor.get_raw_data(token)
        last_close, ma_signal, news_p, news_s = data_processor.normalize_raw_data(ohlcv_raw, news_raw)

        # make new forecast
        oracle = Oracle('token')
        pred, proba = oracle.predict([[ma_signal, news_p, news_s]])

        # save data
        forecast = Forecast(
            token=token,
            last_price=last_close,
            target=pred,
            confidence=proba,
            price_ma_ratio=ma_signal,
            news_polarity=news_p,
            news_subjectivity=news_s
        )
        raw_data = [
            RawData(
                forecast=forecast,
                source_id=SOURCE_BINANCE,
                payload=ohlcv_raw
            ),
            RawData(
                forecast=forecast,
                source_id=SOURCE_NEWSAPI,
                payload=news_raw
            )
        ]
        session.add(forecast)
        session.add_all(raw_data)
        await session.commit()
        # check is_tarin raito > 5 then make train task
        not_trained = await Forecast.get(session=session, token=token, is_trained=False)
        if len(not_trained) > 5:
            print('Пора на тренировку')
            pass
    return forecast

