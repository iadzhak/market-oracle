from sqlmodel import Field

from .base import Base, DateTimeNowField


class Metric(Base, table=True):
    __tablename__ = 'metrics'

    id: int | None = Field(default=None, primary_key=True)
    calculated_at: DateTimeNowField
    close_last: float
    ma_40: float