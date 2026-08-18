from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from .database import engine, Session
from .models import *
from .constants import SOURCES
from .sources import CCXTPriceGetter, NewsApiGetter
from .settings import conf
from .utils import DataProcessor


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with Session() as session:
        await Source.bulk_insert(session=session, data=SOURCES)
        await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.news_getter = NewsApiGetter(
        base_url=conf.NEWS_API_URL,
        api_key=conf.NEWS_API_KEY,
        news_url=conf.NEWS_API_ENDPOINT
    )
    app.state.price_getter = CCXTPriceGetter(conf.CCXT_EXCHANGE)
    app.state.data_processor = DataProcessor(
        price_getter=app.state.price_getter,
        news_getter=app.state.news_getter
    )
    await setup_db()
    yield
    await app.state.price_getter.close()
