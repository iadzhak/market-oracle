from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field, Relationship

from .base import Base


class Source(Base, table=True):
    __tablename__ = 'sources'

    id: str = Field(primary_key=True)
    type: str
    url: str

    @classmethod
    async def bulk_insert(cls, session: AsyncSession, data: list[dict]):
        current_dialect = session.bind.dialect.name
        if current_dialect == 'sqlite':
            stmt = sqlite.insert(cls).values(data).on_conflict_do_update(
                index_elements=[cls.id],
                set_={'type': cls.type, 'url': cls.url}
            )
        elif current_dialect == 'postgresql':
            stmt = postgresql.insert(cls).values(data).on_conflict_do_update(
                index_elements=[cls.id],
                set_={'type': cls.type, 'url': cls.url}
            )
        else:
            raise RuntimeError(f'Bulk insert не поддерживатеся в {current_dialect}')
        await session.execute(stmt)

    raw_data: list['RawData'] = Relationship(back_populates='source')
