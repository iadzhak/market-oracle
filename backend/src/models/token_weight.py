from typing import Optional

from sqlmodel import Field, Column, JSON

from .base import Base

class TokenWeight(Base, table=True):
    __tablename__ = 'token_weights'

    id: str = Field(primary_key=True)
    weights: Optional[dict | list] = Field(default=None, sa_column=Column(JSON, nullable=True))
