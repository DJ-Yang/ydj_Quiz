from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional

from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz import Problem, UserProblemForm, Selection
from app.schemas.quiz import RequestProblemDto


class QuizRepository:
    def __init__(
        self, 
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    async def create_problem(self, data: RequestProblemDto):
        async with self.session_factory() as session:
            problem = Problem(
                title=data.title
            )
            session.add(problem)
            await session.flush()
            await session.refresh(problem)

            await session.execute(insert(Selection).values([
                {
                    "problem_id": problem.id,
                    "content": selection.content,
                    "is_correct": selection.is_correct,
                }
                for selection in data.selections
            ]))
            await session.commit()
            return problem

    async def get_problem_list(self, current_user: int):
        async with self.session_factory() as session:
            stmt = (
                select(Problem)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def delete_problem(self, problem_id: int):
        async with self.session_factory() as session:
            stmt = (
                select(Problem)
                .where(Problem.id == problem_id)
            )
            problem = await session.execute(stmt)
            problem.delete()

    async def get_problem_detail(self, problem_id: int):
        async with self.session_factory() as session:
            stmt = (
                select(Problem)
                .where(Problem.id == problem_id)
                .options(
                    selectinload(Problem.selections)
                )
            )
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

            


    