from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from .database import engine, Session
from .models import *
from .constants import SOURCES


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with Session() as session:
        await Source.bulk_insert(session=session, data=SOURCES)
        await session.commit()
    yield
