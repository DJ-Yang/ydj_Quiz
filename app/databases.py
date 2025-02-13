import logging

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Database:
    def __init__(self, db_url: str, echo: bool) -> None:
        self._engine = create_async_engine(db_url, echo=echo, pool_recycle=3600)
        self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)

    async def connect(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Database Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
