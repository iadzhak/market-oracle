import datetime as dt
from typing import Optional

from sqlalchemy import JSON, Column, func
from sqlmodel import Field, Relationship

from .base import Base


class RawData(Base, table=True):
    __tablename__ = 'raw_data'

    id: int | None = Field(default=None, primary_key=True)
    source_id: str = Field(foreign_key='sources.id')
    forecast_id: int = Field(foreign_key='forecasts.id')
    fetched_at: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))
    payload: Optional[dict | list] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True)
    )

    source: 'Source' = Relationship(back_populates='raw_data')
    forecast: 'Forecast' = Relationship(back_populates='raw_data')
    