from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from .database import Session, engine
from .models import *
from .settings import conf
from .sources import (
    CCXTPriceGetter,
    FakeNewsApiGetter,
    NewsApiGetter,
    NewsBaseSource,
    PriceBaseSource
)
from .utils import DataProcessor


async def setup_db(data: list[dict]):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with Session() as session:
        await Source.bulk_insert(session=session, data=data)
        await session.commit()


def get_news_getter() -> NewsBaseSource:
    if conf.NEWS_FAKER:
        return FakeNewsApiGetter()
    return NewsApiGetter(
        base_url=conf.NEWS_API_URL,
        api_key=conf.NEWS_API_KEY,
        news_url=conf.NEWS_API_ENDPOINT
    )


def get_price_getter() -> PriceBaseSource:
    return CCXTPriceGetter(conf.CCXT_EXCHANGE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    news_getter = get_news_getter()
    app.state.news_getter = news_getter

    price_getter = get_price_getter()
    app.state.price_getter = price_getter

    app.state.data_processor = DataProcessor(
        price_getter=app.state.price_getter,
        news_getter=app.state.news_getter
    )
    await setup_db([news_getter.info(), price_getter.info()])
    yield
    await app.state.price_getter.close()
