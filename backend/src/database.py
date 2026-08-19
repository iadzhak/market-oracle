from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import conf

engine = create_async_engine(conf.DB_URL)
Session = async_sessionmaker(engine, expire_on_commit=False)
