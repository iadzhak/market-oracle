from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import DataProcessor
from .sources import PriceBaseSource, NewsBaseSource
from .database import Session


def get_price_getter(request: Request) -> PriceBaseSource:
    return request.app.state.price_getter


def get_news_getter(request: Request) -> NewsBaseSource:
    return request.app.state.news_getter


def get_data_processor(request: Request) -> DataProcessor:
    return request.app.state.data_processor


async def get_session():
    async with Session() as session:
        yield session


DataProcessorDep = Annotated[DataProcessor, Depends(get_data_processor)]
PriceGetterDep = Annotated[PriceBaseSource, Depends(get_price_getter)]
NewsGetterDep = Annotated[NewsBaseSource, Depends(get_news_getter)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
