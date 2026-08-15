from fastapi import APIRouter

from ..scoring.make_forecast import make_forecast
from ..database import SessionDep
from ..models import Forecast
from ..settings import conf

router = APIRouter(prefix='/api')


@router.get('/tokens')
async def tokens() -> list[str]:
    return conf.AVAILABLE_TOKENS


@router.get('/tokens/{token}')
async def token_info(token: str, session: SessionDep):
    fresh = await Forecast.get_fresh_forecast(session, token)
    if fresh is None:
        raw_data, metric, trend_up = await make_forecast(token)
        session.add(metric)
        session.add_all(raw_data)
        await session.commit()
    return fresh
