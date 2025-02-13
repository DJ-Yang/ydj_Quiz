from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional, Sequence
from fastapi import UploadFile

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    async def is_duplicate_nickname(self, nickname: str) -> Optional[User]:
        async with self.session_factory() as session:
            stmt = select(User).where(User.nickname == nickname)
            result = await session.execute(stmt)
            return result.one_or_none()

    async def create_user(self, nickname: str, device_id: str) -> User:
        async with self.session_factory() as session:
            user = User(
                nickname=nickname,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def get_user_or_none(self, user_id: int) -> Optional[User]:
        async with self.session_factory() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_user_list(self) -> list[User]:
        async with self.session_factory() as session:
            stmt = (
                select(User)
            )
            result = await session.execute(stmt)
            return result.scalars().all()