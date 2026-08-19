from pydantic import BaseModel

from .forecast import Forecast


class ForecastResponse(BaseModel):
    forecast: Forecast
    error_raito: float
    contributions: list[float]
