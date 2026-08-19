import datetime as dt
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field, SQLModel, select

DateTimeNowField = Annotated[dt.datetime,  Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))]


class Base(SQLModel):
    @classmethod
    async def all(cls, session: AsyncSession):
        stmt = select(cls)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        return obj
