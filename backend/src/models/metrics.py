from sqlmodel import Field

from .base import Base, DateTimeNowField


class Metric(Base, table=True):
    __tablename__ = 'metrics'

    id: int | None = Field(default=None, primary_key=True)
    calculated_at: DateTimeNowField
    ma: float
    news_p: float
    news_s: float
