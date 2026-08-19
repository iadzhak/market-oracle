from fastapi import APIRouter, BackgroundTasks

from ..core import Oracle
from ..dependencies import DataProcessorDep, SessionDep
from ..models import Forecast, ForecastResponse, RawData
from ..settings import conf
from ..tasks import perform_partial_fit

router = APIRouter(prefix='/api')


@router.get('/tokens')
async def tokens() -> list[str]:
    return conf.TOKENS


@router.get('/tokens/{token}')
async def token_info(
        token: str,
        session: SessionDep,
        data_processor: DataProcessorDep,
        background_tasks: BackgroundTasks
) -> ForecastResponse:
    token = token.lower()
    forecast = await Forecast.get_fresh_forecast(session, token)
    oracle = Oracle(token)
    if forecast is None:
        # get raw data and metrics
        ohlcv_raw, news_raw = await data_processor.get_raw_data(token)
        last_close, ma_signal, news_p, news_s = data_processor.normalize_raw_data(ohlcv_raw, news_raw)

        # make new forecast
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
                source_id=data_processor.price_getter_id,
                payload=ohlcv_raw
            ),
            RawData(
                forecast=forecast,
                source_id=data_processor.news_getter_id,
                payload=news_raw
            )
        ]
        session.add(forecast)
        session.add_all(raw_data)
        await session.commit()
        # add background task for partial fit
        background_tasks.add_task(perform_partial_fit, token, session, data_processor)
    error_raito = await Forecast.get_error_raito(session, token)
    contributions = oracle.contributions(
        [[forecast.price_ma_ratio, forecast.news_polarity, forecast.news_subjectivity]]
    )
    return ForecastResponse(forecast=forecast, error_raito=error_raito, contributions=list(contributions))
