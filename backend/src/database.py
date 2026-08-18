from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .settings import conf

engine = create_async_engine(conf.DB_URL)
Session = async_sessionmaker(engine, expire_on_commit=False)

